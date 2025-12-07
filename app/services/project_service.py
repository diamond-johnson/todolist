# app/services/project_service.py
from typing import Optional, List

from app.models.project import Project, ProjectId
from app.models.task import Task  # needed for type hints (not used directly here)
from app.core.config import Config
from app.repositories.project_repository import InMemoryProjectRepository
from app.repositories.task_repository import InMemoryTaskRepository
from app.exceptions.service_exceptions import (
    ProjectLimitExceededError,
    DuplicateProjectNameError,
)
from app.exceptions.base import ValidationError


class BaseService:
    """Base service with shared validation logic."""
    def _validate_text(self, text: Optional[str], max_words: int, field: str) -> None:
        if text is None:
            return
        words = text.split()
        if len(words) > max_words:
            raise ValidationError(f"{field} exceeds {max_words} words")


class ProjectService(BaseService):
    """Handles project business logic."""

    def __init__(
        self,
        project_repo: InMemoryProjectRepository,
        task_repo: InMemoryTaskRepository,
        config: Config,
    ) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.config = config

    def create_project(self, name: str, description: Optional[str]) -> Project:
        self._validate_text(name, 30, "Project name")
        self._validate_text(description, 150, "Project description")

        projects = self.project_repo.get_projects()
        if len(projects) >= self.config.max_projects:
            raise ProjectLimitExceededError("Maximum projects exceeded")
        if any(p.name == name for p in projects):
            raise DuplicateProjectNameError(f"Project name '{name}' already exists")

        project = Project(
            id=self.project_repo.get_next_project_id(),
            name=name,
            description=description,
        )
        self.project_repo.add_project(project)
        return project

    def edit_project(
        self,
        project_id: ProjectId,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        project = self.project_repo.get_project(project_id)

        if new_name is not None:
            self._validate_text(new_name, 30, "Project name")
            if new_name != project.name and any(
                p.name == new_name for p in self.project_repo.get_projects()
                if p.id != project_id
            ):
                raise DuplicateProjectNameError(f"Project name '{new_name}' already exists")
            project.name = new_name

        if new_description is not None:
            self._validate_text(new_description, 150, "Project description")
            project.description = new_description

        self.project_repo.update_project(project)
        return project

    def delete_project(self, project_id: ProjectId) -> None:
        self.project_repo.delete_project(project_id)

    def list_projects(self) -> List[Project]:
        return self.project_repo.get_projects()