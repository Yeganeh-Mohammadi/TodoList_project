from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum, Integer, Sequence
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base import Base
import enum

class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"
    
    # Integer autoincrement ID starting from 1 (using Sequence for PostgreSQL)
    id = Column(Integer, Sequence('tasks_id_seq'), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)  # برای تسک‌های بسته شده
    
    # کلید خارجی به Project (با cascade delete در سطح دیتابیس)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"Task(id='{self.id}', title='{self.title}', status='{self.status.value}')"