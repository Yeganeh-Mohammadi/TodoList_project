from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def add(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_by_id(self, project_id: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).first()
    
    def list_all(self) -> List[Project]:
        return self.db.query(Project).all()
    
    def delete(self, project_id: str) -> bool:
        project = self.get_by_id(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False
    
    def update(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return project