from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.project import Project
from app.exceptions.repository_exceptions import ProjectNotFoundError
from typing import List
from . import ProjectRepository


class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, description: str | None = None) -> Project:
        project = Project(name=name, description=description)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get(self, project_id: int) -> Project:
        stmt = select(Project).where(Project.id == project_id)
        result = await self.db.execute(stmt)
        project = result.scalar_one_or_none()
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        return project

    async def get_with_tasks(self, project_id: int) -> Project:
        stmt = select(Project).where(Project.id == project_id).options(selectinload(Project.tasks))
        result = await self.db.execute(stmt)
        project = result.scalar_one_or_none()
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        return project

    async def get_by_name(self, name: str) -> Project | None:
        stmt = select(Project).where(Project.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, project: Project) -> Project:
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete(self, project_id: int) -> None:
        project = await self.get(project_id)
        await self.db.delete(project)
        await self.db.commit()

    async def list_all(self) -> List[Project]:
        stmt = select(Project).order_by(Project.created_at)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        # A more efficient way to count
        result = await self.db.execute(select(Project))
        return len(result.scalars().all())
