from sqlalchemy.orm import Session
from app.models.project import Project
from app.exceptions.repository_exceptions import ProjectNotFoundError
from typing import List
from . import project_repository  # Import abstract

class SQLAlchemyProjectRepository(project_repository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str | None = None) -> Project:
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get(self, project_id: int) -> Project:
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        return project

    def update(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        project = self.get(project_id)
        self.db.delete(project)
        self.db.commit()

    def list_all(self) -> List[Project]:
        return self.db.query(Project).order_by(Project.created_at).all()