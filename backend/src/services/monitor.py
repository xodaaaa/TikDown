from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.core.backoff import random_delay
from src.core.circuit_breaker import CircuitBreaker
from src.core.download_engine import DownloadEngine
from src.db.models.account import MonitoredAccount
from src.db.models.cookie import Cookie
from src.db.models.video import Video
from src.main import event_queue


class MonitorService:
    def __init__(self, db_session_factory):
        self._db_factory = db_session_factory
        self._semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_DOWNLOADS)
        self._circuit_breakers: dict[str, CircuitBreaker] = {}

    async def _get_cb(self, account_id: str) -> CircuitBreaker:
        if account_id not in self._circuit_breakers:
            self._circuit_breakers[account_id] = CircuitBreaker(account_id)
        return self._circuit_breakers[account_id]

    async def check_account(self, account_id: str) -> None:
        async with self._db_factory() as db:
            account = await db.get(MonitoredAccount, account_id)
            if not account or not account.enabled:
                return

            if account.status == "paused":
                return

            cb = await self._get_cb(account_id)
            if cb.is_open:
                return

            engine = await self._build_engine(db, account)

            try:
                await self._emit({
                    "type": "monitor.account_check_started",
                    "payload": {"username": account.tiktok_username},
                })

                entries = await asyncio.to_thread(engine.list_videos, account.tiktok_username)
            except Exception as e:
                cb.record_failure()
                await self._handle_failure(db, account, str(e))
                return

            new_videos = 0
            for entry in entries:
                tiktok_id = entry.get("tiktok_id", "")
                if not tiktok_id:
                    continue

                exists = await db.execute(
                    select(Video).where(Video.tiktok_id == tiktok_id)
                )
                if exists.scalar_one_or_none():
                    continue

                video = Video(
                    monitored_account_id=account.id,
                    tiktok_id=tiktok_id,
                    title=entry.get("title", "")[:512],
                    description=entry.get("description"),
                    upload_date=entry.get("upload_date"),
                    upload_timestamp=entry.get("upload_timestamp"),
                    duration=entry.get("duration"),
                    likes=entry.get("likes", 0),
                    views=entry.get("views", 0),
                    thumbnail_path=entry.get("thumbnail"),
                    status="queued",
                )
                db.add(video)
                new_videos += 1

            account.last_check_at = datetime.now(UTC)
            cb.record_success()
            account.consecutive_failures = 0
            if account.status == "needs_review":
                account.status = "ok"
            await db.commit()

            if new_videos > 0:
                await self._emit({
                    "type": "monitor.new_videos_found",
                    "payload": {"count": new_videos, "account_id": account_id},
                })

    async def download_video(self, video_id: str) -> None:
        async with self._semaphore:
            async with self._db_factory() as db:
                video = await db.get(Video, video_id)
                if not video or video.status == "downloaded":
                    return

                account = await db.get(MonitoredAccount, video.monitored_account_id)
                if not account:
                    return

                engine = await self._build_engine(db, account)

                video.status = "downloading"
                await db.commit()

                try:
                    url = f"https://www.tiktok.com/@{account.tiktok_username}/video/{video.tiktok_id}"
                    info = await engine.download_video_async(url)

                    video.file_path = info.get("requested_downloads", [{}])[0].get("filepath", "")
                    video.file_size = info.get("filesize_approx")
                    video.status = "downloaded"
                    video.downloaded_at = datetime.now(UTC)
                    video.error_text = None

                    await self._emit({
                        "type": "monitor.video_downloaded",
                        "payload": {"title": video.title, "video_id": video_id},
                    })
                except Exception as e:
                    video.retry_count += 1
                    if video.retry_count >= settings.MAX_RETRIES_PER_VIDEO:
                        video.status = "failed"
                        video.error_text = str(e)[:1000]
                    else:
                        video.status = "queued"
                        video.error_text = str(e)[:1000]

                await db.commit()

    async def check_all_accounts(self) -> None:
        async with self._db_factory() as db:
            result = await db.execute(
                select(MonitoredAccount).where(MonitoredAccount.enabled == True)  # noqa: E712
            )
            accounts = list(result.scalars().all())

        usernames = [a.tiktok_username for a in accounts]
        await self._emit({
            "type": "monitor.cycle_started",
            "payload": {"iteration": 0, "accounts": usernames},
        })

        for account in accounts:
            delay = random_delay(settings.MIN_DELAY_SECONDS, settings.MAX_DELAY_SECONDS)
            await asyncio.sleep(delay)
            await self.check_account(account.id)

    async def refresh_profile(self, account_id: str) -> None:
        async with self._db_factory() as db:
            account = await db.get(MonitoredAccount, account_id)
            if not account:
                return

            engine = await self._build_engine(db, account)
            try:
                profile = await asyncio.to_thread(engine.get_profile_info, account.tiktok_username)
                account.avatar_url = profile.get("avatar_url")
                account.follower_count = profile.get("follower_count", 0)
                account.following_count = profile.get("following_count", 0)
                account.total_likes = profile.get("total_likes", 0)
                account.video_count = profile.get("video_count", 0)
                account.profile_last_refreshed = datetime.now(UTC)
            except Exception:
                pass
            await db.commit()

    async def _build_engine(self, db: AsyncSession, account: MonitoredAccount) -> DownloadEngine:
        encrypted = None
        if account.cookie_id:
            cookie = await db.get(Cookie, account.cookie_id)
            if cookie:
                encrypted = cookie.encrypted_content
        return DownloadEngine.build_engine_for_cookies(encrypted)

    async def _handle_failure(self, db: AsyncSession, account: MonitoredAccount, error: str) -> None:
        account.consecutive_failures = (account.consecutive_failures or 0) + 1
        if account.consecutive_failures >= settings.MAX_CONSECUTIVE_FAILURES:
            account.status = "paused"
            await self._emit({
                "type": "monitor.account_paused",
                "payload": {"username": account.tiktok_username, "reason": error[:200]},
            })
        else:
            account.status = "needs_review"
        await db.commit()

    async def _emit(self, event: dict) -> None:
        event["timestamp"] = str(datetime.now(UTC))
        await event_queue.put(event)


monitor_service: MonitorService | None = None


def get_monitor_service() -> MonitorService:
    global monitor_service
    if monitor_service is None:
        from src.db.session import async_session_factory
        monitor_service = MonitorService(async_session_factory)
    return monitor_service
