from typing import Optional, List
from app.models.project import Project
from app.core.config import Config
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.exceptions.service_exceptions import (
    ProjectLimitExceededError,
    DuplicateProjectNameError,
)
from .base_service import BaseService

class ProjectService(BaseService):
    def __init__(self, project_repo: SQLAlchemyProjectRepository, config: Config) -> None:
        self.project_repo = project_repo
        self.config = config

    async def create_project(self, name: str, description: Optional[str] = None) -> Project:
        self._validate_text(name, 30, "Project name")
        self._validate_text(description, 150, "Project description")
        if await self.project_repo.count() >= self.config.max_projects:
            raise ProjectLimitExceededError("Maximum projects exceeded")
        if await self.project_repo.get_by_name(name):
            raise DuplicateProjectNameError(f"Project name '{name}' already exists")
        return await self.project_repo.create(name, description)

    async def edit_project(self, project_id: int, new_name: Optional[str] = None,
                           new_description: Optional[str] = None) -> Project:
        project = await self.project_repo.get(project_id)
        if new_name is not None:
            self._validate_text(new_name, 30, "Project name")
            existing = await self.project_repo.get_by_name(new_name)
            if existing and existing.id != project_id:
                raise DuplicateProjectNameError(f"Project name '{new_name}' already exists")
            project.name = new_name
        if new_description is not None:
            self._validate_text(new_description, 150, "Project description")
            project.description = new_description
        return await self.project_repo.update(project)

    async def delete_project(self, project_id: int) -> None:
        await self.project_repo.delete(project_id)

    async def list_projects(self) -> List[Project]:
        return await self.project_repo.list_all()

    async def get_project_with_tasks(self, project_id: int) -> Project:
        return await self.project_repo.get_with_tasks(project_id)

