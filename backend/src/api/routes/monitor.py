from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_auth
from src.config import settings
from src.db.models.account import MonitoredAccount
from src.db.session import get_db
from src.main import event_queue

router = APIRouter()

_monitor_running = False


@router.get("/status")
async def get_status(request: Request, db: AsyncSession = Depends(get_db)):
    await require_auth(request)

    active = await db.execute(
        select(MonitoredAccount).where(MonitoredAccount.enabled == True)  # noqa: E712
    )
    active_accounts = list(active.scalars().all())

    return {
        "running": _monitor_running,
        "interval_minutes": settings.MONITOR_INTERVAL_MINUTES,
        "next_run": None,
        "last_run": None,
        "active_accounts": len(active_accounts),
        "total_accounts": len(active_accounts),
        "concurrent_downloads": 0,
        "max_concurrent": settings.MAX_CONCURRENT_DOWNLOADS,
    }


@router.post("/start")
async def start_monitor(request: Request, db: AsyncSession = Depends(get_db)):
    global _monitor_running
    await require_auth(request)
    _monitor_running = True

    event = {
        "type": "monitor.cycle_started",
        "payload": {"iteration": 1, "accounts": []},
        "timestamp": str(__import__("datetime").datetime.now(__import__("datetime").timezone.utc)),
    }
    await event_queue.put(event)

    return {"status": "started"}


@router.post("/stop")
async def stop_monitor(request: Request):
    global _monitor_running
    await require_auth(request)
    _monitor_running = False
    return {"status": "stopped"}


@router.post("/check-all")
async def check_all_accounts(request: Request, db: AsyncSession = Depends(get_db)):
    await require_auth(request)

    result = await db.execute(
        select(MonitoredAccount).where(MonitoredAccount.enabled == True)  # noqa: E712
    )
    accounts = list(result.scalars().all())

    event = {
        "type": "monitor.new_videos_found",
        "payload": {"count": 0, "accounts_checked": len(accounts)},
        "timestamp": str(__import__("datetime").datetime.now(__import__("datetime").timezone.utc)),
    }
    await event_queue.put(event)

    return {"checked": len(accounts)}


@router.post("/accounts/{account_id}/check")
async def check_single_account(
    request: Request,
    account_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    account = await db.get(MonitoredAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    event = {
        "type": "monitor.account_check_started",
        "payload": {"username": account.tiktok_username},
        "timestamp": str(__import__("datetime").datetime.now(__import__("datetime").timezone.utc)),
    }
    await event_queue.put(event)

    return {"status": "check_queued", "username": account.tiktok_username}
