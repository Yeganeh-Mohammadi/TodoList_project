"""
Schema definitions using Pydantic for API validation and serialization
"""

from .project import ProjectCreate, ProjectUpdate, ProjectResponse
from .task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus

__all__ = [
    "ProjectCreate",
    "ProjectUpdate", 
    "ProjectResponse",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskStatus",
]

