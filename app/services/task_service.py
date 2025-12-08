from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.models.task import Task
from datetime import datetime
from typing import List

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

    def mark_task_as_done(self, task_id: int) -> Task:
        task = self.get_task_by_id(task_id)
        if task.is_done:
            return task # Already done

        return self.task_repo.update(task, {
            "status": "done",
            "is_done": True,
            "closed_at": datetime.now()
        })

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
                "status": "done",
                "is_done": True,
                "closed_at": datetime.now()
            })
            closed_tasks.append(updated_task)
            
        return closed_tasks