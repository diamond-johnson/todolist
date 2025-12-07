# app/models/project.py
from dataclasses import dataclass, field
from typing import NewType, Optional, List
from datetime import datetime

from app.models.task import Task  # forward reference — needed because Project has tasks


ProjectId = NewType("ProjectId", int)


@dataclass
class Project:
    """Represents a project containing tasks."""
    id: ProjectId
    name: str
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    tasks: List[Task] = field(default_factory=list)