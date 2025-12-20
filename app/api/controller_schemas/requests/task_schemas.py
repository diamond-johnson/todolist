from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from app.models.task import TaskStatus

class TaskCreate(BaseModel):
    """Schema for creating a new task within a project."""
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus = Field(TaskStatus.TODO, description="Initial status of the task.")
    deadline: Optional[date] = None

class TaskUpdate(BaseModel):
    """Schema for updating a task. All fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None
    deadline: Optional[date] = None
