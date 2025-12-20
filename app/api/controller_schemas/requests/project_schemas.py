from pydantic import BaseModel, Field
from typing import Optional

class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str = Field(..., min_length=1, max_length=100, description="The name of the project.")
    description: Optional[str] = Field(None, max_length=500, description="An optional description for the project.")

class ProjectUpdate(BaseModel):
    """Schema for updating an existing project. All fields are optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="The new name of the project.")
    description: Optional[str] = Field(None, max_length=500, description="The new description for the project.")
