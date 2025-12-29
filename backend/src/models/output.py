from sqlite3 import Date
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from backend.src.db.base import Base

class Output(Base):
    __tablename__ = "outputs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("ai_tasks.id"))
    gen_file_path: Mapped[str] = mapped_column(String)
    source_filenames: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)