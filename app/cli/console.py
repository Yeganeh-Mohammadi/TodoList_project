from app.db.session import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from datetime import datetime, timedelta

# Function to setup services using Dependency Injection
def setup_services(db):
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    
    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_repo)
    
    return project_service, task_service

def run_test_cli():
    """A minimal CLI to demonstrate creation and autoclose functionality."""
    print("\n--- Running CLI Demonstration (Phase 2) ---")
    
    with get_db() as db:
        project_service, task_service = setup_services(db)

        # 1. Create a Project
        try:
            print("1. Creating Project: 'Daily Tasks'")
            project = project_service.create_project(name="Daily Tasks", description="Tasks for today")
            print(f"   -> Project created (ID: {project.id})")
        except ValueError as e:
            # If already exists, fetch it
            project = project_service.project_repo.get_by_name("Daily Tasks")
            if not project:
                 raise e # re-raise if something else is wrong

        project_id = project.id

        # 2. Create an OVERDUE task (for autoclose test)
        deadline_past = datetime.now() - timedelta(hours=1)
        print("2. Creating Overdue Task...")
        task_service.create_task(
            title="Overdue Test Task", 
            project_id=project_id, 
            deadline=deadline_past
        )
        print("   -> Overdue task created.")

        # 3. Create an OPEN task (should not be closed)
        deadline_future = datetime.now() + timedelta(days=1)
        print("3. Creating Open Task...")
        task_service.create_task(
            title="Future Task", 
            project_id=project_id, 
            deadline=deadline_future
        )
        print("   -> Future task created.")
        
        # 4. Run the autoclose command logic
        print("\n--- Running autoclose-overdue logic via Service ---")
        closed_tasks = task_service.autoclose_overdue_tasks()
        
        print(f"RESULT: {len(closed_tasks)} tasks were closed automatically.")
        if closed_tasks:
            print(f"Closed task: {closed_tasks[0].title} (Status: {closed_tasks[0].status})")

    print("\n--- CLI Demonstration Finished ---")