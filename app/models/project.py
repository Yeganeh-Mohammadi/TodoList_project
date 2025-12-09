from sqlalchemy import Column, String, DateTime, Text, Integer, Sequence
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base import Base

class Project(Base):
    __tablename__ = "projects"
    
    # Integer autoincrement ID starting from 1 (using Sequence for PostgreSQL)
    id = Column(Integer, Sequence('projects_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # رابطه با Task
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Project(id='{self.id}', name='{self.name}')"
    