from app.repositories.project_repository import ProjectRepository
from app.models.project import Project
from typing import List

class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        # Dependency Injection: Service depends on Repository
        self.project_repo = project_repo

    def create_project(self, name: str, description: str = None) -> Project:
        # Business logic: Check for duplicate name before creation
        if self.project_repo.get_by_name(name):
            raise ValueError(f"Project with name '{name}' already exists.")

        project_data = {
            "name": name,
            "description": description
        }
        # Repository handles the data access (creating the ORM object)
        return self.project_repo.create(project_data)

    def get_all_projects(self) -> List[Project]:
        return self.project_repo.get_all()

    def get_project_by_id(self, project_id: str) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found.")
        return project

    def delete_project(self, project_id: str) -> None:
        project = self.get_project_by_id(project_id)
        # Cascade delete is handled by ORM setup (in app/models/project.py)
        self.project_repo.delete(project)