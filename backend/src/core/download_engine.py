from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget

from src.config import settings
from src.core.crypto import decrypt_cookies


class DownloadEngine:
    def __init__(self, cookiefile_path: str | None = None):
        self._cookiefile_path = cookiefile_path
        self._opts: dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "format": "best",
            "outtmpl": str(Path(settings.MEDIA_DIR) / "%(uploader)s" / "%(id)s.%(ext)s"),
            "socket_timeout": 30,
            "retries": 3,
            "fragment_retries": 3,
            "impersonate": ImpersonateTarget.from_str("chrome"),
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            "extractor_args": {
                "tiktok": {
                    "api_hostname": "api16-normal-c-useast1a.tiktokv.com",
                }
            },
        }
        if cookiefile_path:
            self._opts["cookiefile"] = cookiefile_path

    def _build_opts(self, **overrides: Any) -> dict[str, Any]:
        opts = {**self._opts, **overrides}
        return opts

    def extract_info(self, url: str, download: bool = False) -> dict[str, Any]:
        opts = self._build_opts()
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=download)

    async def extract_info_async(self, url: str, download: bool = False) -> dict[str, Any]:
        import asyncio
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.extract_info, url, download)

    def download_video(self, url: str, **extra_opts: Any) -> dict[str, Any]:
        opts = self._build_opts(**extra_opts)
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=True)

    async def download_video_async(self, url: str, **extra_opts: Any) -> dict[str, Any]:
        import asyncio
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.download_video, url, **extra_opts)

    def check_account_available(self, username: str) -> dict[str, Any]:
        url = f"https://www.tiktok.com/@{username}"
        return self.extract_info(url, download=False)

    def get_profile_info(self, username: str) -> dict[str, Any]:
        url = f"https://www.tiktok.com/@{username}"
        info = self.extract_info(url, download=False, process=False)
        return {
            "avatar_url": info.get("uploader_thumbnail") or info.get("thumbnail"),
            "follower_count": info.get("channel_follower_count") or 0,
            "following_count": info.get("channel_following_count") or 0,
            "total_likes": info.get("like_count") or 0,
            "video_count": info.get("playlist_count") or 0,
        }

    def list_videos(self, username: str) -> list[dict[str, Any]]:
        url = f"https://www.tiktok.com/@{username}"
        info = self.extract_info(url, download=False)
        entries = []
        if info and "entries" in info:
            for entry in info["entries"]:
                if entry:
                    entries.append({
                        "tiktok_id": str(entry.get("id", "")),
                        "title": entry.get("title", ""),
                        "description": entry.get("description"),
                        "upload_date": entry.get("upload_date"),
                        "upload_timestamp": entry.get("timestamp"),
                        "duration": entry.get("duration"),
                        "likes": entry.get("like_count") or 0,
                        "views": entry.get("view_count") or 0,
                        "url": entry.get("webpage_url") or entry.get("url"),
                        "thumbnail": entry.get("thumbnail"),
                    })
        return entries

    @staticmethod
    def build_engine_for_cookies(encrypted_cookies: str | None) -> DownloadEngine:
        if not encrypted_cookies:
            return DownloadEngine()
        cookiefile_path = _write_temp_cookiefile(encrypted_cookies)
        return DownloadEngine(cookiefile_path=cookiefile_path)


def _write_temp_cookiefile(encrypted_cookies: str) -> str:
    raw = decrypt_cookies(encrypted_cookies)
    fd, path = tempfile.mkstemp(suffix=".txt", prefix="tikdown_cookies_")
    with os.fdopen(fd, "w") as f:
        f.write(raw)
    return path
