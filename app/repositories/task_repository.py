from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.task import Task, TaskStatus
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):

    def __init__(self, db: Session):
        super().__init__(db)

    def create(self, task_data: Dict[str, Any]) -> Task:
        """ایجاد تسک جدید"""
        task = Task(**task_data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def add(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all(self) -> List[Task]:
        """همه تسک‌ها را برمی‌گرداند"""
        return self.db.query(Task).all()

    def list_all(self) -> List[Task]:
        return self.db.query(Task).all()

    def list_by_project(self, project_id: str) -> List[Task]:
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .all()
        )

    def delete(self, task: Task) -> None:
        """حذف تسک"""
        self.db.delete(task)
        self.db.commit()

    def update(self, task: Task, task_data: Dict[str, Any] = None) -> Task:
        """به‌روزرسانی تسک"""
        if task_data:
            for key, value in task_data.items():
                setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_overdue_and_open_tasks(self) -> List[Task]:
        """تسک‌های گذشته‌ای که هنوز باز هستند را برمی‌گرداند"""
        now = datetime.utcnow()
        return (
            self.db.query(Task)
            .filter(
                Task.deadline < now,
                Task.status != TaskStatus.DONE
            )
            .all()
        )

    def close_overdue_tasks(self) -> int:
        """Auto-close tasks whose due dates are passed."""
        now = datetime.utcnow()

        overdue_tasks = (
            self.db.query(Task)
            .filter(Task.deadline < now, Task.status != TaskStatus.DONE)
            .all()
        )

        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = now

        self.db.commit()
        return len(overdue_tasks)
