class TodoListError(Exception):
    """Base class for TodoList-related errors."""


class ProjectError(TodoListError):
    """Base class for project-related errors."""


class ProjectNotFoundError(ProjectError):
    """Raised when a project is not found."""


class DuplicateProjectNameError(ProjectError):
    """Raised when a project name is duplicate."""


class ProjectLimitExceededError(ProjectError):
    """Raised when maximum projects limit is exceeded."""


class TaskError(TodoListError):
    """Base class for task-related errors."""


class TaskNotFoundError(TaskError):
    """Raised when a task is not found."""


class TaskLimitExceededError(TaskError):
    """Raised when maximum tasks limit is exceeded."""


class InvalidStatusError(TaskError):
    """Raised when an invalid task status is provided."""


class InvalidDeadlineError(TaskError):
    """Raised when an invalid deadline format is provided."""


class ValidationError(TodoListError):
    """Raised for general validation failures."""