from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.task import Task
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):

    def __init__(self, db: Session):
        super().__init__(db)

    def add(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def list_all(self) -> List[Task]:
        return self.db.query(Task).all()

    def list_by_project(self, project_id: int) -> List[Task]:
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .all()
        )

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def close_overdue_tasks(self) -> int:
        """Auto-close tasks whose due dates are passed."""
        now = datetime.utcnow()

        overdue_tasks = (
            self.db.query(Task)
            .filter(Task.due_date < now, Task.status != "CLOSED")
            .all()
        )

        for task in overdue_tasks:
            task.status = "CLOSED"

        self.db.commit()
        return len(overdue_tasks)
