from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, project_data: Dict[str, Any]) -> Project:
        """ایجاد پروژه جدید"""
        project = Project(**project_data)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def add(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).first()
    
    def get_all(self) -> List[Project]:
        """همه پروژه‌ها را برمی‌گرداند"""
        return self.db.query(Project).all()
    
    def list_all(self) -> List[Project]:
        return self.db.query(Project).all()
    
    def delete(self, project: Project) -> None:
        """حذف پروژه (cascade delete تسک‌ها به صورت خودکار انجام می‌شود)"""
        self.db.delete(project)
        self.db.commit()
    
    def update(self, project: Project, project_data: Dict[str, Any] = None) -> Project:
        """به‌روزرسانی پروژه"""
        if project_data:
            for key, value in project_data.items():
                setattr(project, key, value)
        self.db.commit()
        self.db.refresh(project)
        return project