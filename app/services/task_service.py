from typing import Optional, List
from datetime import datetime
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.core.config import Config
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.exceptions.service_exceptions import (
    TaskLimitExceededError,
    InvalidStatusError,
    InvalidDeadlineError,
)
from app.exceptions.base import ValidationError
from .base_service import BaseService

class TaskService(BaseService):
    """Service for managing tasks, enforcing status, deadlines, and limits."""

    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository, config: Config) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.config = config

    def _parse_deadline(self, deadline_str: Optional[str]) -> Optional[datetime]:
        """Parse deadline string to datetime, raising error on invalid format."""
        if not deadline_str:
            return None
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise InvalidDeadlineError("Invalid deadline format (use YYYY-MM-DD)")

    def create_task(self, project_id: int, title: str, description: Optional[str] = None,
                    status: str = "todo", deadline_str: Optional[str] = None) -> Task:
        """Create a new task in a project, checking limits and validating inputs."""
        self._validate_text(title, 30, "Task title")
        self._validate_text(description, 150, "Task description")
        try:
            status_enum = TaskStatus(status.lower())
        except ValueError:
            raise InvalidStatusError(f"Invalid status '{status}'")
        project = self.project_repo.get(project_id)
        if len(self.task_repo.list_by_project(project)) >= self.config.max_tasks:
            raise TaskLimitExceededError("Maximum tasks per project exceeded")
        deadline = self._parse_deadline(deadline_str)
        return self.task_repo.create(project, title, description, status_enum, deadline)

    def change_task_status(self, project_id: int, task_id: int, new_status: str) -> Task:
        """Change task status, auto-closing if done."""
        try:
            status_enum = TaskStatus(new_status.lower())
        except ValueError:
            raise InvalidStatusError(f"Invalid status '{new_status}'")
        project = self.project_repo.get(project_id)
        task = self.task_repo.get(task_id)
        if task.project_id != project.id:
            raise ValidationError("Task does not belong to project")
        task.status = status_enum
        if status_enum == TaskStatus.DONE and task.closed_at is None:
            task.closed_at = datetime.utcnow()
        return self.task_repo.update(task)

    def edit_task(self, project_id: int, task_id: int, new_title: Optional[str] = None,
                  new_description: Optional[str] = None, new_status: Optional[str] = None,
                  new_deadline_str: Optional[str] = None) -> Task:
        """Edit task details, validating changes and ownership."""
        project = self.project_repo.get(project_id)
        task = self.task_repo.get(task_id)
        if task.project_id != project.id:
            raise ValidationError("Task does not belong to project")
        if new_title is not None:
            self._validate_text(new_title, 30, "Task title")
            task.title = new_title
        if new_description is not None:
            self._validate_text(new_description, 150, "Task description")
            task.description = new_description
        if new_status is not None:
            try:
                status_enum = TaskStatus(new_status.lower())
            except ValueError:
                raise InvalidStatusError(f"Invalid status '{new_status}'")
            task.status = status_enum
            if status_enum == TaskStatus.DONE and task.closed_at is None:
                task.closed_at = datetime.utcnow()
        if new_deadline_str is not None:
            task.deadline = self._parse_deadline(new_deadline_str)
        return self.task_repo.update(task)

    def delete_task(self, project_id: int, task_id: int) -> None:
        """Delete a task, validating ownership."""
        project = self.project_repo.get(project_id)
        task = self.task_repo.get(task_id)
        if task.project_id != project.id:
            raise ValidationError("Task does not belong to project")
        self.task_repo.delete(task_id)

    def list_tasks(self, project_id: int) -> List[Task]:
        """List tasks for a project."""
        project = self.project_repo.get(project_id)
        return self.task_repo.list_by_project(project)