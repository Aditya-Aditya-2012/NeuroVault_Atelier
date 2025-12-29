from sqlalchemy import Boolean, String, Integer, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from backend.src.db.base import Base

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String)
    file_path: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String), default=[], server_default='{}')
