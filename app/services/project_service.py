from typing import Optional, List
from app.models.project import Project
from app.core.config import Config
from app.repositories import project_repository
from app.exceptions.service_exceptions import (
    ProjectLimitExceededError,
    DuplicateProjectNameError,
)
from app.exceptions.base import ValidationError

class BaseService:
    def _validate_text(self, text: Optional[str], max_words: int, field: str) -> None:
        if text is None:
            return
        words = text.split()
        if len(words) > max_words:
            raise ValidationError(f"{field} exceeds {max_words} words")

class ProjectService(BaseService):
    def __init__(self, project_repo: project_repository, config: Config) -> None:
        self.project_repo = project_repo
        self.config = config

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        self._validate_text(name, 30, "Project name")
        self._validate_text(description, 150, "Project description")
        if len(self.project_repo.list_all()) >= self.config.max_projects:
            raise ProjectLimitExceededError("Maximum projects exceeded")
        if self.project_repo.db.query(Project).filter(Project.name == name).first():
            raise DuplicateProjectNameError(f"Project name '{name}' already exists")
        return self.project_repo.create(name, description)

    def edit_project(self, project_id: int, new_name: Optional[str] = None,
                     new_description: Optional[str] = None) -> Project:
        project = self.project_repo.get(project_id)
        if new_name is not None:
            self._validate_text(new_name, 30, "Project name")
            if new_name != project.name and self.project_repo.db.query(Project).filter(Project.name == new_name).first():
                raise DuplicateProjectNameError(f"Project name '{new_name}' already exists")
            project.name = new_name
        if new_description is not None:
            self._validate_text(new_description, 150, "Project description")
            project.description = new_description
        return self.project_repo.update(project)

    def delete_project(self, project_id: int) -> None:
        self.project_repo.delete(project_id)

    def list_projects(self) -> List[Project]:
        return self.project_repo.list_all()