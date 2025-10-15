from datetime import datetime
from models import Project, Task


class ToDoService:
    def __init__(self, storage):
        self.storage = storage

    # Project operations 
    def create_project(self, name: str, description: str = "") -> Project:
        project = Project(name=name, description=description)
        self.storage.add_project(project)
        return project

    def list_projects(self):
        return self.storage.list_projects()

    def delete_project(self, proid: str):
        project = self.storage.get_project(proid)
        if not project:
            raise ValueError(f"Project '{proid}' not found.")
        
        self.storage.remove_project(project.id)

    # Task operations
    def add_task(self, proid: str, title: str, description: str = "", deadline: str = "") -> Task:
        project = self.storage.get_project(proid)
        if not project:
            raise ValueError(f"Project '{proid}' not found.")
            
        task = Task(title=title, description=description, deadline=deadline)
        project.tasks.append(task)
        project.updated_at = datetime.utcnow()
        return task

    def list_tasks(self, proid: str):
        project = self.storage.get_project(proid)
        if not project:
            raise ValueError(f"Project '{proid}' not found.")
        return project.tasks
    
    def update_task_status(self, project_identifier: str, task_identifier: str, new_status: str) -> Task:
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
