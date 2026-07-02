from datetime import datetime

from pydantic import BaseModel


class MonitorStatus(BaseModel):
    running: bool
    interval_minutes: int
    next_run: datetime | None = None
    last_run: datetime | None = None
    active_accounts: int
    total_accounts: int
    concurrent_downloads: int
    max_concurrent: int


class MonitorConfig(BaseModel):
    interval_minutes: int | None = None
    max_concurrent_downloads: int | None = None
    min_delay_seconds: int | None = None
    max_delay_seconds: int | None = None
