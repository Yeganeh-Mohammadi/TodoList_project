from app.db.session import get_db
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.task import TaskStatus
from datetime import datetime

def setup_services(db):
    """تنظیم سرویس‌ها"""
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    project_service = ProjectService(project_repo)
    task_service = TaskService(task_repo, project_repo)
    return project_service, task_service

def parse_datetime(date_string: str) -> datetime:
    """Parse date string to datetime"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Invalid date format: {date_string}. Valid format: YYYY-MM-DD or YYYY-MM-DD HH:MM")

def task_create(title: str, project_id: int, description: str = None, deadline: str = None):
    """Create a new task"""
    try:
        deadline_dt = None
        if deadline:
            deadline_dt = parse_datetime(deadline)
        
        with get_db() as db:
            project_service, task_service = setup_services(db)
            task = task_service.create_task(title, project_id, description, deadline_dt)
            print(f"Success: Task '{task.title}' created successfully!")
            print(f"   ID: {task.id}")
            print(f"   Status: {task.status.value}")
            if deadline_dt:
                print(f"   Deadline: {deadline_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def task_list(project_id: int = None):
    """List tasks"""
    try:
        with get_db() as db:
            project_service, task_service = setup_services(db)
            
            if project_id:
                tasks = task_service.get_tasks_by_project(project_id)
                project = project_service.get_project_by_id(project_id)
                print(f"\nTasks for project '{project.name}':")
            else:
                tasks = task_service.get_all_tasks()
                print(f"\nAll Tasks:")
            
            if not tasks:
                print("No tasks found.")
                return
            
            print("="*60)
            status_emoji = {"todo": "📝", "doing": "🔄", "done": "✅"}
            
            for i, task in enumerate(tasks, 1):
                emoji = status_emoji.get(task.status.value, "📋")
                print(f"\n{i}. {emoji} {task.title} (ID: {task.id})")
                print(f"   Status: {task.status.value}")
                # Display project name
                if task.project:
                    print(f"   Project: {task.project.name} (ID: {task.project.id})")
                if task.description:
                    print(f"   Description: {task.description}")
                if task.deadline:
                    is_overdue = task.deadline < datetime.utcnow() and task.status != TaskStatus.DONE
                    overdue_mark = " ⚠️ OVERDUE" if is_overdue else ""
                    print(f"   Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M:%S')}{overdue_mark}")
                if task.closed_at:
                    print(f"   Closed at: {task.closed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60 + "\n")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def task_update_status(task_id: int, status_str: str):
    """Update task status"""
    try:
        # Convert string to enum
        status_map = {
            "todo": TaskStatus.TODO,
            "doing": TaskStatus.DOING,
            "done": TaskStatus.DONE
        }
        
        status_str_lower = status_str.lower()
        if status_str_lower not in status_map:
            print(f"Error: Invalid status: {status_str}")
            print("   Valid statuses: todo, doing, done")
            return
        
        status = status_map[status_str_lower]
        
        with get_db() as db:
            project_service, task_service = setup_services(db)
            
            # Get task before update to show old status
            task_before = task_service.get_task_by_id(task_id)
            old_status = task_before.status.value
            
            # Update status
            task = task_service.update_task_status(task_id, status)
            
            # Display result
            print(f"Success: Task '{task.title}' status updated!")
            print(f"   Previous status: {old_status}")
            print(f"   New status: {status.value}")
            if task.project:
                print(f"   Project: {task.project.name} (ID: {task.project.id})")
            if status == TaskStatus.DONE and task.closed_at:
                print(f"   Closed at: {task.closed_at.strftime('%Y-%m-%d %H:%M:%S')}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def task_delete(task_id: int):
    """Delete a task"""
    try:
        with get_db() as db:
            project_service, task_service = setup_services(db)
            task = task_service.get_task_by_id(task_id)
            task_title = task.title
            task_service.delete_task(task_id)
            print(f"Success: Task '{task_title}' deleted successfully!")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def task_show(task_id: int):
    """Show task details"""
    try:
        with get_db() as db:
            project_service, task_service = setup_services(db)
            task = task_service.get_task_by_id(task_id)
            project = project_service.get_project_by_id(task.project_id)
            
            status_emoji = {"todo": "📝", "doing": "🔄", "done": "✅"}
            emoji = status_emoji.get(task.status.value, "📋")
            
            print("\n" + "="*60)
            print(f"{emoji} Task: {task.title}")
            print("="*60)
            print(f"ID: {task.id}")
            print(f"Status: {task.status.value}")
            print(f"Project: {project.name} (ID: {project.id})")
            if task.description:
                print(f"Description: {task.description}")
            if task.deadline:
                is_overdue = task.deadline < datetime.utcnow() and task.status != TaskStatus.DONE
                overdue_mark = " ⚠️ OVERDUE" if is_overdue else ""
                print(f"Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M:%S')}{overdue_mark}")
            print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if task.closed_at:
                print(f"Closed at: {task.closed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60 + "\n")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def task_schedule(task_id: int, deadline: str):
    """Set or update task deadline"""
    try:
        deadline_dt = parse_datetime(deadline)
        
        with get_db() as db:
            project_service, task_service = setup_services(db)
            task = task_service.get_task_by_id(task_id)
            task_service.task_repo.update(task, {"deadline": deadline_dt})
            print(f"Success: Task '{task.title}' deadline set to '{deadline_dt.strftime('%Y-%m-%d %H:%M:%S')}'!")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

