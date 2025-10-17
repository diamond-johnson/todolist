from dataclasses import dataclass, field

from typing import NewType, Literal, Optional

from datetime import datetime

ProjectId = NewType("ProjectId", int)
TaskId = NewType("TaskId", int)
TaskStatus = Literal["todo", "doing", "done"]


@dataclass
class Task:
    """Represents a task in the To-Do List."""

    id: TaskId
    title: str
    description: str
    status: TaskStatus
    deadline: Optional[datetime]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Project:
    """Represents a project containing tasks."""

    id: ProjectId
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    tasks: list[Task] = field(default_factory=list)