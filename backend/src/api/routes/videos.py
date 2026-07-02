from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routes.auth import require_auth
from src.db.models.video import Video
from src.db.session import get_db
from src.schemas.video import VideoBulkAction, VideoListResponse, VideoResponse

router = APIRouter()


@router.get("", response_model=VideoListResponse)
async def list_videos(
    request: Request,
    account_id: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)

    query = select(Video)
    if account_id:
        query = query.where(Video.monitored_account_id == account_id)
    if status:
        query = query.where(Video.status == status)
    if search:
        query = query.where(Video.title.ilike(f"%{search}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    offset = (page - 1) * page_size
    result = await db.execute(
        query.order_by(Video.created_at.desc()).offset(offset).limit(page_size)
    )
    videos = list(result.scalars().all())

    return VideoListResponse(videos=videos, total=total, page=page, page_size=page_size)


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    request: Request,
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    video = await db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/{video_id}/file")
async def get_video_file(
    request: Request,
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    video = await db.get(Video, video_id)
    if not video or not video.file_path:
        raise HTTPException(status_code=404, detail="Video file not found")
    if not os.path.exists(video.file_path):
        raise HTTPException(status_code=404, detail="Video file missing from disk")
    return FileResponse(video.file_path, media_type="video/mp4")


@router.post("/{video_id}/retry", response_model=VideoResponse)
async def retry_video(
    request: Request,
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    video = await db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.status = "queued"
    video.error_text = None
    await db.commit()
    await db.refresh(video)
    return video


@router.delete("/{video_id}", status_code=204)
async def delete_video(
    request: Request,
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)
    video = await db.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if video.file_path and os.path.exists(video.file_path):
        try:
            os.remove(video.file_path)
        except OSError:
            pass
    await db.delete(video)
    await db.commit()


@router.post("/bulk", status_code=200)
async def bulk_action(
    request: Request,
    data: VideoBulkAction,
    db: AsyncSession = Depends(get_db),
):
    await require_auth(request)

    result = await db.execute(select(Video).where(Video.id.in_(data.video_ids)))
    videos = list(result.scalars().all())

    if data.action == "delete":
        for video in videos:
            if video.file_path and os.path.exists(video.file_path):
                try:
                    os.remove(video.file_path)
                except OSError:
                    pass
            await db.delete(video)
    elif data.action == "retry":
        for video in videos:
            video.status = "queued"
            video.error_text = None
    elif data.action == "download":
        for video in videos:
            if video.status != "downloaded":
                video.status = "queued"

    await db.commit()
    return {"processed": len(videos)}
