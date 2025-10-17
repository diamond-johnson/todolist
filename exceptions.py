from __future__ import annotations


class ToDoListError(Exception):
    """Base class for ToDoList-related errors."""


class InvalidTaskStatusError(ToDoListError):
    """Raised when an invalid task status is provided."""


class TaskLimitExceededError(ToDoListError):
    """Raised when task limit is exceeded."""


class InvalidTaskDataError(ToDoListError):
    """Raised when task data (e.g., title, description) is invalid."""


class ProjectLimitExceededError(ToDoListError):
    """Raised when project limit is exceeded."""


class InvalidProjectDataError(ToDoListError):
    """Raised when project data (e.g., name, description) is invalid."""


class ProjectNotFoundError(ToDoListError):
    """Raised when a project is not found."""


class TaskNotFoundError(ToDoListError):
    """Raised when a task is not found in a project."""


class DuplicateProjectNameError(ToDoListError):
    """Raised when a project name is duplicate."""