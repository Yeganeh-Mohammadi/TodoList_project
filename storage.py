from typing import Dict
from .models import Project


class InMemoryStorage:

    def __init__(self):
        self._projects: Dict[str, Project] = {}

    def add_project(self, project: Project):
        self._projects[project.id] = project

    def get_project(self, project_id: str) -> Project:
        #get project with id
        return self._projects.get(project_id)

    def remove_project(self, project_id: str):
        if project_id in self._projects:
            del self._projects[project_id]

    def list_projects(self):
        return list(self._projects.values())
