from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class MonitoredAccount(Base):
    __tablename__ = "monitored_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tiktok_username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(20), default="ok")
    consecutive_failures: Mapped[int] = mapped_column(Integer, default=0)
    last_check_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_video_timestamp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    options_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    cookie_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    follower_count: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    following_count: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    total_likes: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    video_count: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    profile_last_refreshed: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    videos = relationship("Video", back_populates="account", cascade="all, delete-orphan")
    events = relationship("ActivityEvent", back_populates="account", cascade="all, delete-orphan")
