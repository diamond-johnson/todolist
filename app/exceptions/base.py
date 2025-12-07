class TodoListError(Exception):
    """Base exception for the entire application."""
    pass


class ValidationError(TodoListError):
    """Raised for general validation failures."""
    pass