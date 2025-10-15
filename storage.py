from models import Project
from typing import Dict, Optional


class InMemoryStorage:

    def __init__(self):
        self._projects: Dict[str, Project] = {}

    def add_project(self, project: Project):
        self._projects[project.id] = project

    def get_project(self, id: str) -> Optional[Project]:
        if id in self._projects:
            return self._projects[id]

        for pid, project in self._projects.items():
            if pid.startswith(id):
                return project
        
        for project in self._projects.values():
            if project.name.lower() == id.lower():
                return project

        return None


    def remove_project(self, project_id: str):
        if project_id in self._projects:
            del self._projects[project_id]

    def list_projects(self):
        return list(self._projects.values())