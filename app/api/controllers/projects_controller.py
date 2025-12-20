from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.project_service import ProjectService
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.core.config import Config
from app.api.controller_schemas.requests import project_schemas
from app.api.controller_schemas.responses import project_schemas as project_responses

router = APIRouter()

# Dependency for ProjectService
def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    repo = SQLAlchemyProjectRepository(db)
    return ProjectService(repo, Config())

@router.post(
    "/",
    response_model=project_responses.ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
async def create_project(
    project_in: project_schemas.ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project with a name and an optional description.
    """
    project = await service.create_project(name=project_in.name, description=project_in.description)
    return project

@router.get("/", response_model=List[project_responses.ProjectResponse], summary="List all projects")
async def list_projects(service: ProjectService = Depends(get_project_service)):
    """
    Retrieve a list of all projects.
    """
    return await service.list_projects()

@router.get("/{project_id}", response_model=project_responses.ProjectDetailResponse, summary="Get a specific project")
async def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    """
    Get detailed information for a single project by its ID, including all its tasks.
    """
    return await service.get_project_with_tasks(project_id)


@router.put("/{project_id}", response_model=project_responses.ProjectResponse, summary="Update a project")
async def update_project(
    project_id: int,
    project_in: project_schemas.ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """
    Update a project's name or description.
    """
    project = await service.edit_project(
        project_id,
        new_name=project_in.name,
        new_description=project_in.description
    )
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a project")
async def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    """
    Delete a project and all its associated tasks.
    """
    await service.delete_project(project_id)
    return None
