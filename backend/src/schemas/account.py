from datetime import datetime

from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    tiktok_username: str = Field(min_length=1, max_length=255)
    enabled: bool = True
    cookie_id: str | None = None


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    enabled: bool | None = None
    cookie_id: str | None = None
    status: str | None = None


class AccountProfile(BaseModel):
    avatar_url: str | None = None
    follower_count: int | None = 0
    following_count: int | None = 0
    total_likes: int | None = 0
    video_count: int | None = 0
    profile_last_refreshed: datetime | None = None


class AccountResponse(AccountBase):
    id: str
    status: str
    consecutive_failures: int
    last_check_at: datetime | None = None
    last_video_timestamp: int | None = None
    avatar_url: str | None = None
    follower_count: int | None = 0
    following_count: int | None = 0
    total_likes: int | None = 0
    video_count: int | None = 0
    profile_last_refreshed: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]
    total: int
