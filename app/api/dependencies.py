"""
Dependencies for FastAPI endpoints
وابستگی‌های مورد نیاز برای endpointهای FastAPI
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.db.session import SessionLocal, engine
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def get_db() -> Session:
    """
    Dependency برای دریافت database session
    
    این dependency:
    - یک session جدید ایجاد می‌کند
    - آن را به endpoint می‌دهد
    - بعد از اتمام درخواست، session را می‌بندد
    - در صورت خطا، rollback می‌کند
    """
    db = SessionLocal()
    try:
        yield db
        # اگر repositoryها commit نکردند، اینجا commit می‌کنیم
        # اما چون repositoryها خودشان commit می‌کنند، این خط معمولاً اجرا نمی‌شود
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise
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
    
    این dependency:
    - یک session از get_db دریافت می‌کند
    - Repositoryها را با این session ایجاد می‌کند
    - Service را با repositoryها ایجاد می‌کند
    - Service را به endpoint می‌دهد
    """
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return TaskService(task_repo, project_repo)


def check_db_connection():
    """
    بررسی اتصال به دیتابیس
    برای استفاده در startup event
    """
    try:
        # تست اتصال با یک query ساده
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to connect to database: {str(e)}")

