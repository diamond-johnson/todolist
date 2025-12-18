from typing import Optional, List
from app.models.project import Project
from app.core.config import Config
from app.repositories.project_repository import ProjectRepository  # Fixed import to concrete class
from app.exceptions.service_exceptions import (
    ProjectLimitExceededError,
    DuplicateProjectNameError,
)
from app.exceptions.base import ValidationError
from .base_service import BaseService

class ProjectService(BaseService):
    """Service for managing projects, enforcing business rules like limits and uniqueness."""

    def __init__(self, project_repo: ProjectRepository, config: Config) -> None:
        self.project_repo = project_repo
        self.config = config

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """Create a new project, checking limits and uniqueness for data integrity."""
        self._validate_text(name, 30, "Project name")
        self._validate_text(description, 150, "Project description")
        if len(self.project_repo.list_all()) >= self.config.max_projects:
            raise ProjectLimitExceededError("Maximum projects exceeded")
        if any(p.name == name for p in self.project_repo.list_all()):  # Use repo for check (no direct DB)
            raise DuplicateProjectNameError(f"Project name '{name}' already exists")
        return self.project_repo.create(name, description)

    def edit_project(self, project_id: int, new_name: Optional[str] = None,
                     new_description: Optional[str] = None) -> Project:
        """Edit project details, ensuring name uniqueness if changed."""
        project = self.project_repo.get(project_id)
        if new_name is not None:
            self._validate_text(new_name, 30, "Project name")
            if new_name != project.name and any(p.name == new_name for p in self.project_repo.list_all()):  # Use repo for check (no direct DB)
                raise DuplicateProjectNameError(f"Project name '{new_name}' already exists")
            project.name = new_name
        if new_description is not None:
            self._validate_text(new_description, 150, "Project description")
            project.description = new_description
        return self.project_repo.update(project)

    def delete_project(self, project_id: int) -> None:
        """Delete a project by ID, cascading to tasks via relationship."""
        self.project_repo.delete(project_id)

    def list_projects(self) -> List[Project]:
        """List all projects, sorted by creation time."""
        return self.project_repo.list_all()