# app/commands/autoclose_overdue.py

from app.db.session import get_db
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.services.task_service import TaskService
from app.services.project_service import ProjectService # Added for completeness

def autoclose_overdue_command():
    """
    Python command to automatically close overdue and open tasks.
    This function handles the setup of dependencies (Dependency Injection).
    """
    print("Running autoclose-overdue command...")

    # Use the context manager to get a transactional database session
    with get_db() as db:
        # Setup Repositories and Service
        task_repo = TaskRepository(db)
        project_repo = ProjectRepository(db)
        # Note: We only need TaskService for autoclose logic
        task_service = TaskService(task_repo, project_repo) 

        # Execute the core business logic
        closed_tasks = task_service.autoclose_overdue_tasks()
        
        if closed_tasks:
            print(f"Successfully closed {len(closed_tasks)} overdue tasks:")
            for task in closed_tasks:
                print(f"  - Task ID: {task.id}, Title: {task.title}, Closed At: {task.closed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("No overdue tasks found to close.")