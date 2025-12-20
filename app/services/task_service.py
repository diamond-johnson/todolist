from typing import Optional, List
from datetime import datetime
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.core.config import Config
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.exceptions.service_exceptions import (
    TaskLimitExceededError,
    InvalidStatusError,
    InvalidDeadlineError,
)
from app.exceptions.base import ValidationError
from .base_service import BaseService

class TaskService(BaseService):
    def __init__(self, project_repo: SQLAlchemyProjectRepository, task_repo: SQLAlchemyTaskRepository, config: Config) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo
        self.config = config

    def _parse_deadline(self, deadline_str: Optional[str]) -> Optional[datetime]:
        """(No change needed) This is a synchronous, pure-logic function."""
        if not deadline_str:
            return None
        try:
            # Assuming deadline is passed as YYYY-MM-DD date string
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise InvalidDeadlineError("Invalid deadline format (use YYYY-MM-DD)")

    async def create_task(self, project_id: int, title: str, description: Optional[str] = None,
                          status: str = "todo", deadline_str: Optional[str] = None) -> Task:
        """Asynchronously create a new task."""
        self._validate_text(title, 30, "Task title")
        self._validate_text(description, 150, "Task description")
        try:
            status_enum = TaskStatus(status.lower())
        except ValueError:
            raise InvalidStatusError(f"Invalid status '{status}'")

        project = await self.project_repo.get(project_id)
        tasks = await self.task_repo.list_by_project(project)
        if len(tasks) >= self.config.max_tasks:
            raise TaskLimitExceededError("Maximum tasks per project exceeded")

        deadline = self._parse_deadline(deadline_str)
        return await self.task_repo.create(project, title, description, status_enum, deadline)

    async def change_task_status(self, project_id: int, task_id: int, new_status: str) -> Task:
        """Asynchronously change a task's status."""
        try:
            status_enum = TaskStatus(new_status.lower())
        except ValueError:
            raise InvalidStatusError(f"Invalid status '{new_status}'")

        project = await self.project_repo.get(project_id)
        task = await self.task_repo.get(task_id)
        if task.project_id != project.id:
            raise ValidationError("Task does not belong to the specified project")

        task.status = status_enum
        if status_enum == TaskStatus.DONE and task.closed_at is None:
            task.closed_at = datetime.utcnow()
        elif status_enum != TaskStatus.DONE:
            task.closed_at = None # Re-open the task if status is changed from done

        return await self.task_repo.update(task)

    async def edit_task(self, project_id: int, task_id: int, new_title: Optional[str] = None,
                        new_description: Optional[str] = None, new_status: Optional[str] = None,
                        new_deadline_str: Optional[str] = None) -> Task:
        """Asynchronously edit task details."""
        project = await self.project_repo.get(project_id)
        task = await self.task_repo.get(task_id)
        if task.project_id != project.id:
            raise ValidationError("Task does not belong to the specified project")

        if new_title is not None:
            self._validate_text(new_title, 30, "Task title")
            task.title = new_title
        if new_description is not None:
            self._validate_text(new_description, 150, "Task description")
            task.description = new_description
        if new_status is not None:
            try:
                status_enum = TaskStatus(new_status.lower())
                task.status = status_enum
                if status_enum == TaskStatus.DONE and task.closed_at is None:
                    task.closed_at = datetime.utcnow()
                elif status_enum != TaskStatus.DONE:
                    task.closed_at = None
            except ValueError:
                raise InvalidStatusError(f"Invalid status '{new_status}'")
        if new_deadline_str is not None:
            task.deadline = self._parse_deadline(new_deadline_str)

        return await self.task_repo.update(task)

    async def delete_task(self, project_id: int, task_id: int) -> None:
        """Asynchronously delete a task."""
        project = await self.project_repo.get(project_id)
        task = await self.task_repo.get(task_id) # Ensure task exists before checking ownership
        if task.project_id != project.id:
            raise ValidationError("Task does not belong to the specified project")
        await self.task_repo.delete(task_id)

    async def list_tasks(self, project_id: int) -> List[Task]:
        """Asynchronously list tasks for a project."""
        project = await self.project_repo.get(project_id)
        return await self.task_repo.list_by_project(project)
