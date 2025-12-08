from app.db.session import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

def setup_services(db):
    """تنظیم سرویس‌ها"""
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_repo)
    return project_service, task_service

def project_help():
    """Show project commands help"""
    print("\nProject Commands:")
    print("  python main.py project create <name> [description]")
    print("  python main.py project list")
    print("  python main.py project delete <project_id>")
    print("  python main.py project show <project_id>")
    print("  python main.py project help")

def project_create(name: str, description: str = None):
    """Create a new project"""
    try:
        with get_db() as db:
            project_service, _ = setup_services(db)
            project = project_service.create_project(name, description)
            print(f"Success: Project '{project.name}' created successfully!")
            print(f"   ID: {project.id}")
            if description:
                print(f"   Description: {description}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def project_list():
    """List all projects"""
    try:
        with get_db() as db:
            project_service, task_service = setup_services(db)
            projects = project_service.get_all_projects()
            
            if not projects:
                print("No projects found.")
                return
            
            print("\nProject List:")
            print("="*60)
            for project in projects:
                tasks = task_service.get_tasks_by_project(project.id)
                print(f"\n{project.name} (ID: {project.id})")
                if project.description:
                    print(f"   Description: {project.description}")
                print(f"   Tasks: {len(tasks)}")
                print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Error: {e}")

def project_delete(project_id: str):
    """Delete a project (tasks will be automatically deleted)"""
    try:
        with get_db() as db:
            project_service, task_service = setup_services(db)
            
            # Show project tasks before deletion
            tasks = task_service.get_tasks_by_project(project_id)
            project = project_service.get_project_by_id(project_id)
            
            print(f"Deleting project '{project.name}'...")
            if tasks:
                print(f"   {len(tasks)} task(s) will also be automatically deleted.")
            
            project_service.delete_project(project_id)
            print(f"Success: Project '{project.name}' and {len(tasks)} task(s) deleted successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def project_show(project_id: str):
    """Show project details and its tasks"""
    try:
        with get_db() as db:
            project_service, task_service = setup_services(db)
            project = project_service.get_project_by_id(project_id)
            tasks = task_service.get_tasks_by_project(project_id)
            
            print("\n" + "="*60)
            print(f"Project: {project.name}")
            print("="*60)
            print(f"ID: {project.id}")
            if project.description:
                print(f"Description: {project.description}")
            print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Updated: {project.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            print(f"\nTasks ({len(tasks)}):")
            if tasks:
                for i, task in enumerate(tasks, 1):
                    status_emoji = {"todo": "📝", "doing": "🔄", "done": "✅"}
                    emoji = status_emoji.get(task.status.value, "📋")
                    print(f"\n  {i}. {emoji} {task.title}")
                    print(f"     Status: {task.status.value}")
                    if task.description:
                        print(f"     Description: {task.description}")
                    if task.deadline:
                        print(f"     Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M:%S')}")
                    if task.closed_at:
                        print(f"     Closed at: {task.closed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("  No tasks found.")
            print("="*60 + "\n")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
