from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .task_schemas import TaskResponse # Import TaskResponse for nesting

class ProjectResponse(BaseModel):
    """Schema for a single project response."""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectDetailResponse(ProjectResponse):
    """Schema for a single project including its tasks."""
    tasks: List[TaskResponse] = []
