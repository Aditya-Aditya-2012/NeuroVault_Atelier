from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from backend.src.db.base import Base

class TaskStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AITask(Base):
    __tablename__ = "ai_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    prompt: Mapped[str] = mapped_column(String, nullable=True)
    input_image_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False) 
    status: Mapped[str] = mapped_column(Enum(TaskStatus), default="Taskstatus.PENDING")