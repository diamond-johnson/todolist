from .base import TodoListError


class ProjectNotFoundError(TodoListError):
    """Raised when a project is not found in repository."""
    pass


class TaskNotFoundError(TodoListError):
    """Raised when a task is not found in repository."""
    pass