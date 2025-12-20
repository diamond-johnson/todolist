from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.task_service import TaskService
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.core.config import Config
from app.api.controller_schemas.requests import task_schemas
from app.api.controller_schemas.responses import task_schemas as task_responses

router = APIRouter()

# Dependency for TaskService
def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    project_repo = SQLAlchemyProjectRepository(db)
    task_repo = SQLAlchemyTaskRepository(db)
    return TaskService(project_repo, task_repo, Config())

@router.post(
    "/",
    response_model=task_responses.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task in a project"
)
async def create_task(
    project_id: int,
    task_in: task_schemas.TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """
    Create a new task within a specified project.
    """
    task = await service.create_task(
        project_id=project_id,
        title=task_in.title,
        description=task_in.description,
        status=task_in.status.value,
        deadline_str=str(task_in.deadline) if task_in.deadline else None
    )
    return task

@router.get("/", response_model=List[task_responses.TaskResponse], summary="List tasks in a project")
async def list_tasks(project_id: int, service: TaskService = Depends(get_task_service)):
    """
    Retrieve all tasks associated with a specific project.
    """
    return await service.list_tasks(project_id)

@router.patch(
    "/{task_id}",
    response_model=task_responses.TaskResponse,
    summary="Update a task"
)
async def update_task(
    project_id: int,
    task_id: int,
    task_in: task_schemas.TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """
    Partially update a task's details, such as title, description, status, or deadline.
    Only provided fields will be updated.
    """
    task = await service.edit_task(
        project_id=project_id,
        task_id=task_id,
        new_title=task_in.title,
        new_description=task_in.description,
        new_status=task_in.status.value if task_in.status else None,
        new_deadline_str=str(task_in.deadline) if task_in.deadline else None
    )
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
async def delete_task(project_id: int, task_id: int, service: TaskService = Depends(get_task_service)):
    """
    Delete a specific task from a project.
    """
    await service.delete_task(project_id, task_id)
    return None
