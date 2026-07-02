from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    monitored_account_id: Mapped[str] = mapped_column(String(36), ForeignKey("monitored_accounts.id"), index=True)
    tiktok_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(512), default="")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    upload_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    upload_timestamp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    thumbnail_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    likes: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    views: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    error_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    downloaded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    account = relationship("MonitoredAccount", back_populates="videos")
