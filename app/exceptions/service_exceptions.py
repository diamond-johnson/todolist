from .base import TodoListError


class ProjectError(TodoListError):
    """Base class for project-related business errors."""
    pass


class TaskError(TodoListError):
    """Base class for task-related business errors."""
    pass


class DuplicateProjectNameError(ProjectError):
    """Raised when a project name already exists."""
    pass


class ProjectLimitExceededError(ProjectError):
    """Raised when maximum projects limit is exceeded."""
    pass


class TaskLimitExceededError(TaskError):
    """Raised when maximum tasks per project is exceeded."""
    pass


class InvalidStatusError(TaskError):
    """Raised when an invalid task status is provided."""
    pass


class InvalidDeadlineError(TaskError):
    """Raised when an invalid deadline format is provided."""
    pass