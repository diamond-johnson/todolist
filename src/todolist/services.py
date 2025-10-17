from typing import Optional, get_args

from datetime import datetime

from .models import Project, Task, ProjectId, TaskId, TaskStatus

from .storage import Storage

from .config import Config

from .exceptions import (
    ValidationError,
    ProjectLimitExceededError,
    DuplicateProjectNameError,
    TaskLimitExceededError,
    InvalidStatusError,
    InvalidDeadlineError,
)


class BaseService:
    """Base service with shared validation logic."""
    def _validate_text(self, text: Optional[str], max_words: int, field: str) -> None:
        """Validate text word count if provided."""
        if text is None:
            return
        words = text.split()
        if len(words) > max_words:
            raise ValidationError(f"{field} exceeds {max_words} words")


class ProjectService(BaseService):
    """Handles project business logic."""
    def __init__(self, storage: Storage, config: Config) -> None:
        self.storage = storage
        self.config = config

    def create_project(self, name: str, description: Optional[str]) -> Project:
        """Create a new project with validation."""
        self._validate_text(name, 30, "Project name")
        self._validate_text(description, 150, "Project description")
        if len(self.storage.get_projects()) >= self.config.max_projects:
            raise ProjectLimitExceededError("Maximum projects exceeded")
        if any(p.name == name for p in self.storage.get_projects()):
            raise DuplicateProjectNameError(f"Project name '{name}' already exists")
        project = Project(
            id=self.storage.get_next_project_id(),
            name=name,
            description=description,
        )
        self.storage.add_project(project)
        return project

    def edit_project(
        self,
        project_id: ProjectId,
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
    ) -> Project:
        """Edit project details with validation."""
        project = self.storage.get_project(project_id)
        if new_name is not None:
            self._validate_text(new_name, 30, "Project name")
            if new_name != project.name and any(
                p.name == new_name for p in self.storage.get_projects() if p.id != project_id
            ):
                raise DuplicateProjectNameError(f"Project name '{new_name}' already exists")
            project.name = new_name
        if new_description is not None:
            self._validate_text(new_description, 150, "Project description")
            project.description = new_description
        self.storage.update_project(project)
        return project

    def delete_project(self, project_id: ProjectId) -> None:
        """Delete project and cascade delete tasks."""
        self.storage.delete_project(project_id)

    def list_projects(self) -> list[Project]:
        """List all projects sorted by creation time."""
        return self.storage.get_projects()


class TaskService(BaseService):
    """Handles task business logic."""
    def __init__(self, storage: Storage, config: Config) -> None:
        self.storage = storage
        self.config = config

    def _parse_deadline(self, deadline_str: Optional[str]) -> Optional[datetime]:
        """Parse deadline string to datetime."""
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
        """Create a new task with validation."""
        self._validate_text(title, 30, "Task title")
        self._validate_text(description, 150, "Task description")
        if status not in get_args(TaskStatus):
            raise InvalidStatusError(f"Invalid status '{status}'")
        project = self.storage.get_project(project_id)
        if len(project.tasks) >= self.config.max_tasks:
            raise TaskLimitExceededError("Maximum tasks per project exceeded")
        task = Task(
            id=self.storage.get_next_task_id(),
            title=title,
            description=description,
            status=status,
            deadline=self._parse_deadline(deadline_str),
        )
        self.storage.add_task(project_id, task)
        return task

    def change_task_status(
        self, project_id: ProjectId, task_id: TaskId, new_status: TaskStatus
    ) -> Task:
        """Change task status with validation."""
        if new_status not in get_args(TaskStatus):
            raise InvalidStatusError(f"Invalid status '{new_status}'")
        task = self.storage.get_task(project_id, task_id)
        task.status = new_status
        self.storage.update_task(project_id, task)
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
        """Edit task details with validation."""
        task = self.storage.get_task(project_id, task_id)
        if new_title is not None:
            self._validate_text(new_title, 30, "Task title")
            task.title = new_title
        if new_description is not None:
            self._validate_text(new_description, 150, "Task description")
            task.description = new_description
        if new_status is not None:
            if new_status not in get_args(TaskStatus):
                raise InvalidStatusError(f"Invalid status '{new_status}'")
            task.status = new_status
        if new_deadline_str is not None:
            task.deadline = self._parse_deadline(new_deadline_str)
        self.storage.update_task(project_id, task)
        return task

    def delete_task(self, project_id: ProjectId, task_id: TaskId) -> None:
        """Delete a task."""
        self.storage.delete_task(project_id, task_id)

    def list_tasks(self, project_id: ProjectId) -> list[Task]:
        """List tasks in a project sorted by creation time."""
        return self.storage.get_tasks(project_id)