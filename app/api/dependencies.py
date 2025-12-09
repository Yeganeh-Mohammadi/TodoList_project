"""
Dependencies for FastAPI endpoints
وابستگی‌های مورد نیاز برای endpointهای FastAPI
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def get_db() -> Session:
    """
    Dependency برای دریافت database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """
    Dependency برای دریافت ProjectService
    """
    project_repo = ProjectRepository(db)
    return ProjectService(project_repo)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """
    Dependency برای دریافت TaskService
    """
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return TaskService(task_repo, project_repo)

