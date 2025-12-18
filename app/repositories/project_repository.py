from sqlalchemy.orm import Session
from app.models.project import Project
from app.exceptions.repository_exceptions import ProjectNotFoundError
from typing import List
from . import ProjectRepository
from typing import cast, List
from sqlalchemy import select

class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str | None = None) -> Project:
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get(self, project_id: int) -> Project:
        stmt = select(Project).where(Project.id == project_id)
        project = self.db.execute(stmt).scalar_one_or_none()
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
        stmt = select(Project).order_by(Project.created_at)
        return list(self.db.execute(stmt).scalars().all())