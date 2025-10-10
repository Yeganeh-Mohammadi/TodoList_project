from datetime import datetime
from .models import Project, Task


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

    def delete_project(self, project_id: str):
        self.storage.remove_project(project_id)

    # Task operations
    def add_task(self, project_id: str, title: str, description: str = "", deadline: str = "") -> Task:
        project = self.storage.get_project(project_id)
        if not project:
            raise ValueError("Project not found.")
        task = Task(title=title, description=description, deadline=deadline)
        project.tasks.append(task)
        project.updated_at = datetime.utcnow()
        return task

    def list_tasks(self, project_id: str):
        project = self.storage.get_project(project_id)
        if not project:
            raise ValueError("Project not found.")
        return project.tasks

