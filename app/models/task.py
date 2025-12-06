from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..db.base import Base
import enum

class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)  # برای تسک‌های بسته شده
    
    # کلید خارجی به Project
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"Task(id='{self.id}', title='{self.title}', status='{self.status.value}')"