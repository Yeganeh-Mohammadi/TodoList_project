from datetime import datetime
from models import Project, Task
from dateutil.parser import parse, ParserError # NEW: For date validation
import config # NEW: For reading limits


class ToDoService:
    def __init__(self, storage):
        self.storage = storage

    # Project operations 
    def create_project(self, name: str, description: str = "") -> Project:
        
        # AC (1) - Max Number of Projects check [cite: 57, 136]
        if len(self.storage.list_projects()) >= config.MAX_NUMBER_OF_PROJECT:
            raise ValueError(f"Max number of projects ({config.MAX_NUMBER_OF_PROJECT}) reached.")

        # AC (1) - Uniqueness check 
        if self.storage.get_project(name) is not None:
             raise ValueError(f"Project name '{name}' already exists.")

        # AC (1) - Word/Char limits check 
        if len(name) > config.MAX_PROJECT_NAME_CHARS:
            raise ValueError(f"Project name is too long (Max {config.MAX_PROJECT_NAME_CHARS} characters).")
        if len(description) > config.MAX_PROJECT_DESC_CHARS:
            raise ValueError(f"Project description is too long (Max {config.MAX_PROJECT_DESC_CHARS} characters).")
        
        project = Project(name=name, description=description)
        self.storage.add_project(project)
        return project

    def list_projects(self):
        # AC (8) - Sorted by creation time 
        projects = self.storage.list_projects()
        return sorted(projects, key=lambda p: p.created_at)

    def delete_project(self, proid: str):
        project = self.storage.get_project(proid)
        if not project:
            raise ValueError(f"Project '{proid}' not found.")
        
        # Cascade Delete is handled implicitly because tasks are nested in the Project object
        self.storage.remove_project(project.id)

    # Task operations
    def add_task(self, proid: str, title: str, description: str = "", deadline: str = "") -> Task:
        project = self.storage.get_project(proid)
        if not project:
            raise ValueError(f"Project '{proid}' not found.")
            
        # AC (4) - Max Number of Tasks check [cite: 85, 136]
        if len(project.tasks) >= config.MAX_NUMBER_OF_TASK_PER_PROJECT:
            raise ValueError(f"Max number of tasks ({config.MAX_NUMBER_OF_TASK_PER_PROJECT}) reached in project '{project.name}'.")

        # AC (4) - Title/Desc limits check [cite: 81]
        if len(title) > config.MAX_TASK_TITLE_CHARS:
            raise ValueError(f"Task title is too long (Max {config.MAX_TASK_TITLE_CHARS} characters).")
        if len(description) > config.MAX_TASK_DESC_CHARS:
            raise ValueError(f"Task description is too long (Max {config.MAX_TASK_DESC_CHARS} characters).")

        # AC (4) - Valid deadline check 
        if deadline:
            try:
                parse(deadline)
            except (ValueError, ParserError):
                raise ValueError(f"Invalid deadline format: '{deadline}'. Please use a recognizable date format.")

        task = Task(title=title, description=description, deadline=deadline)
        project.tasks.append(task)
        project.updated_at = datetime.utcnow()
        return task

    def list_tasks(self, proid: str):
        project = self.storage.get_project(proid)
        if not project:
            raise ValueError(f"Project '{proid}' not found.")
        return project.tasks
    
    # NEW: Implement delete_task (AC 7) 
    def delete_task(self, project_identifier: str, task_identifier: str):
        project = self.storage.get_project(project_identifier)
        if not project:
            raise ValueError(f"Project '{project_identifier}' not found.")
        
        # Find task by ID prefix or Title 
        task_to_remove = None
        for task in project.tasks:
            if task.id.startswith(task_identifier) or task.title.lower() == task_identifier.lower():
                task_to_remove = task
                break
        
        if task_to_remove:
            project.tasks.remove(task_to_remove)
            project.updated_at = datetime.utcnow()
        else:
            raise ValueError(f"Task with ID prefix or Title '{task_identifier}' not found in project '{project.name}'.")


    def update_task_status(self, project_identifier: str, task_identifier: str, new_status: str) -> Task:
        # ... (This method was already compliant with AC 5 validation) [cite: 95]
        project = self.storage.get_project(project_identifier)
        if not project:
            raise ValueError(f"Project '{project_identifier}' not found.")
        
        valid_statuses = ["todo", "doing", "done"]
        if new_status.lower() not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")


        for task in project.tasks:
            if task.id.startswith(task_identifier):
                task.status = new_status.lower()
                project.updated_at = datetime.utcnow()
                return task
            
            if task.title.lower() == task_identifier.lower():
                task.status = new_status.lower()
                project.updated_at = datetime.utcnow()
                return task

        raise ValueError(f"Task with ID prefix or Title '{task_identifier}' not found in project '{project.name}'.")