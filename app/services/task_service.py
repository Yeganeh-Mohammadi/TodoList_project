from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.models.task import Task, TaskStatus
from datetime import datetime
from typing import List, Optional

class TaskService:
    # Dependency Injection: Service depends on Repository interface
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self.task_repo = task_repo
        self.project_repo = project_repo

    # --- CRUD Operations ---

    def create_task(self, title: str, project_id: int, description: str = None, deadline: datetime = None) -> Task:
        # Business logic: Check if project exists
        if not self.project_repo.get_by_id(project_id):
            raise ValueError(f"Project with ID {project_id} not found.")

        task_data = {
            "title": title,
            "project_id": project_id,
            "description": description,
            "deadline": deadline,
        }
        return self.task_repo.create(task_data)
    
    def get_task_by_id(self, task_id: int) -> Task:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        return task

    def get_all_tasks(self) -> List[Task]:
        """همه تسک‌ها را برمی‌گرداند"""
        return self.task_repo.get_all()

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """تسک‌های یک پروژه را برمی‌گرداند"""
        return self.task_repo.list_by_project(project_id)

    def update_task(
        self, 
        task_id: int, 
        title: str = None, 
        description: str = None, 
        deadline: datetime = None, 
        status: TaskStatus = None
    ) -> Task:
        """به‌روزرسانی تسک"""
        task = self.get_task_by_id(task_id)
        
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if deadline is not None:
            update_data["deadline"] = deadline
        if status is not None:
            update_data["status"] = status
            # اگر status به DONE تغییر کرد، closed_at را تنظیم کن
            if status == TaskStatus.DONE and task.status != TaskStatus.DONE:
                update_data["closed_at"] = datetime.utcnow()
            elif status != TaskStatus.DONE:
                update_data["closed_at"] = None
        
        return self.task_repo.update(task, update_data)

    def update_task_status(self, task_id: int, status: TaskStatus) -> Task:
        """به‌روزرسانی وضعیت تسک"""
        task = self.get_task_by_id(task_id)
        
        update_data = {"status": status}
        if status == TaskStatus.DONE and task.status != TaskStatus.DONE:
            update_data["closed_at"] = datetime.utcnow()
        elif status != TaskStatus.DONE:
            update_data["closed_at"] = None
            
        return self.task_repo.update(task, update_data)

    def mark_task_as_done(self, task_id: int) -> Task:
        """علامت‌گذاری تسک به عنوان انجام شده"""
        return self.update_task_status(task_id, TaskStatus.DONE)

    def delete_task(self, task_id: int) -> None:
        """حذف تسک"""
        task = self.get_task_by_id(task_id)
        self.task_repo.delete(task)

    # --- Autoclose Logic (Scheduled Command) ---
    
    def autoclose_overdue_tasks(self) -> List[Task]:
        """
        Business Logic to close overdue and open tasks.
        """
        overdue_tasks = self.task_repo.get_overdue_and_open_tasks()
        closed_tasks = []

        for task in overdue_tasks:
            # We use the update function from the repository
            updated_task = self.task_repo.update(task, {
                "status": TaskStatus.DONE,
                "closed_at": datetime.utcnow()
            })
            closed_tasks.append(updated_task)
            
        return closed_tasks