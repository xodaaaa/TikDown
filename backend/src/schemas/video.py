from datetime import datetime

from pydantic import BaseModel, Field


class VideoResponse(BaseModel):
    id: str
    monitored_account_id: str
    tiktok_id: str
    title: str
    description: str | None = None
    upload_date: str | None = None
    upload_timestamp: int | None = None
    duration: int | None = None
    file_path: str | None = None
    file_size: int | None = None
    thumbnail_path: str | None = None
    likes: int | None = 0
    views: int | None = 0
    status: str
    error_text: str | None = None
    retry_count: int
    downloaded_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class VideoListResponse(BaseModel):
    videos: list[VideoResponse]
    total: int
    page: int = 1
    page_size: int = 20


class VideoFilter(BaseModel):
    account_id: str | None = None
    status: str | None = None
    search: str | None = None


class VideoBulkAction(BaseModel):
    video_ids: list[str]
    action: str = Field(pattern="^(delete|retry|download)$")
