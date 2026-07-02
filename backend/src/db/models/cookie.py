from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Cookie(Base):
    __tablename__ = "cookies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(255))
    account_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    original_format: Mapped[str] = mapped_column(String(10), default="txt")
    encrypted_content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="unverified")
    last_validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
