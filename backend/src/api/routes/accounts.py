from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_auth
from src.db.models.account import MonitoredAccount
from src.db.session import get_db
from src.schemas.account import AccountCreate, AccountListResponse, AccountResponse, AccountUpdate

router = APIRouter()


@router.get("", response_model=AccountListResponse)
async def list_accounts(
    request: Request,
    search: str | None = Query(None),
    show_disabled: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    query = select(MonitoredAccount)
    if search:
        query = query.where(MonitoredAccount.tiktok_username.ilike(f"%{search}%"))
    if not show_disabled:
        query = query.where(MonitoredAccount.enabled == True)  # noqa: E712

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    result = await db.execute(query.order_by(MonitoredAccount.created_at.desc()))
    accounts = list(result.scalars().all())

    return AccountListResponse(accounts=accounts, total=total)


@router.post("", response_model=AccountResponse, status_code=201)
async def create_account(
    request: Request,
    data: AccountCreate,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)

    existing = await db.execute(
        select(MonitoredAccount).where(MonitoredAccount.tiktok_username == data.tiktok_username)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Account already exists")

    account = MonitoredAccount(**data.model_dump())
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    request: Request,
    account_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    account = await db.get(MonitoredAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.patch("/{account_id}", response_model=AccountResponse)
async def update_account(
    request: Request,
    account_id: str,
    data: AccountUpdate,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    account = await db.get(MonitoredAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(account, key, value)

    await db.commit()
    await db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=204)
async def delete_account(
    request: Request,
    account_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    account = await db.get(MonitoredAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await db.delete(account)
    await db.commit()
