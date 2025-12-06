from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..db.base import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # رابطه با Task
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Project(id='{self.id}', name='{self.name}')"
    