# app/models/task.py
from dataclasses import dataclass, field
from typing import NewType, Literal, Optional
from datetime import datetime


TaskId = NewType("TaskId", int)
TaskStatus = Literal["todo", "doing", "done"]


@dataclass
class Task:
    """Represents a task in the To-Do List."""
    id: TaskId
    title: str
    description: Optional[str] = None
    status: TaskStatus = "todo"
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)