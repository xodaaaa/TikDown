from datetime import datetime

from pydantic import BaseModel


class CookieResponse(BaseModel):
    id: str
    name: str
    account_id: str | None = None
    original_format: str
    status: str
    last_validated_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class CookieTestResponse(BaseModel):
    id: str
    status: str
    message: str
    validated_at: datetime


class CookieListResponse(BaseModel):
    cookies: list[CookieResponse]
