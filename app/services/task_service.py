# app/services/task_service.py
from typing import Optional
from datetime import datetime

from app.models.project import Project, ProjectId
from app.models.task import Task, TaskId, TaskStatus
from app.core.config import Config
from app.repositories.project_repository import InMemoryProjectRepository
from app.repositories.task_repository import InMemoryTaskRepository
from app.exceptions.service_exceptions import (
    TaskLimitExceededError,
    InvalidStatusError,
    InvalidDeadlineError,
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


class TaskService(BaseService):
    """Handles task business logic."""

    def __init__(
        self,
        project_repo: InMemoryProjectRepository,
        task_repo: InMemoryTaskRepository,
        config: Config,
    ) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.config = config

    def _parse_deadline(self, deadline_str: Optional[str]) -> Optional[datetime]:
        if not deadline_str:
            return None
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise InvalidDeadlineError("Invalid deadline format (use YYYY-MM-DD)")

    def create_task(
        self,
        project_id: ProjectId,
        title: str,
        description: Optional[str],
        status: TaskStatus = "todo",
        deadline_str: Optional[str] = None,
    ) -> Task:
        self._validate_text(title, 30, "Task title")
        self._validate_text(description, 150, "Task description")
        if status not in ("todo", "doing", "done"):
            raise InvalidStatusError(f"Invalid status '{status}'")

        project = self.project_repo.get_project(project_id)
        if len(project.tasks) >= self.config.max_tasks:
            raise TaskLimitExceededError("Maximum tasks per project exceeded")

        task = Task(
            id=self.task_repo.get_next_task_id(),
            title=title,
            description=description,
            status=status,
            deadline=self._parse_deadline(deadline_str),
        )
        self.task_repo.add_task(project, task)
        return task

    def change_task_status(
        self, project_id: ProjectId, task_id: TaskId, new_status: TaskStatus
    ) -> Task:
        if new_status not in ("todo", "doing", "done"):
            raise InvalidStatusError(f"Invalid status '{new_status}'")

        project = self.project_repo.get_project(project_id)
        task = self.task_repo.get_task(project, task_id)
        task.status = new_status
        self.task_repo.update_task(project, task)
        return task

    def edit_task(
        self,
        project_id: ProjectId,
        task_id: TaskId,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_status: Optional[TaskStatus] = None,
        new_deadline_str: Optional[str] = None,
    ) -> Task:
        project = self.project_repo.get_project(project_id)
        task = self.task_repo.get_task(project, task_id)

        if new_title is not None:
            self._validate_text(new_title, 30, "Task title")
            task.title = new_title
        if new_description is not None:
            self._validate_text(new_description, 150, "Task description")
            task.description = new_description
        if new_status is not None:
            if new_status not in ("todo", "doing", "done"):
                raise InvalidStatusError(f"Invalid status '{new_status}'")
            task.status = new_status
        if new_deadline_str is not None:
            task.deadline = self._parse_deadline(new_deadline_str)

        self.task_repo.update_task(project, task)
        return task

    def delete_task(self, project_id: ProjectId, task_id: TaskId) -> None:
        project = self.project_repo.get_project(project_id)
        self.task_repo.delete_task(project, task_id)

    def list_tasks(self, project_id: ProjectId) -> list[Task]:
        project = self.project_repo.get_project(project_id)
        return self.task_repo.get_tasks(project)