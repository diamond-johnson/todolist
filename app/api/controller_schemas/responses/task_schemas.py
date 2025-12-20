from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.task import TaskStatus

class TaskResponse(BaseModel):
    """Schema for a single task response."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    deadline: Optional[date]
    created_at: datetime
    closed_at: Optional[datetime]
    project_id: int

    class Config:
        orm_mode = True
