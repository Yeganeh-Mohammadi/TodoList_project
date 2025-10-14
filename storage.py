from typing import Dict
from .models import Project


class InMemoryStorage:

    def __init__(self):
        self._projects: Dict[str, Project] = {}

    def add_project(self, project: Project):
        self._projects[project.id] = project

    def get_project(self, project_id: str) -> Project:
    # Try exact match first
        if project_id in self._projects:
                return self._projects[project_id]

    # Then try partial match (prefix)
    for pid, project in self._projects.items():
        if pid.startswith(project_id):
            return project

      return None


    def remove_project(self, project_id: str):
        if project_id in self._projects:
            del self._projects[project_id]

    def list_projects(self):
        return list(self._projects.values())
