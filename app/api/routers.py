from fastapi import APIRouter
from .controllers import projects_controller, tasks_controller

api_router = APIRouter()

# Include the projects router
api_router.include_router(projects_controller.router, prefix="/projects", tags=["Projects"])

# Include the tasks router nested under projects
api_router.include_router(tasks_controller.router, prefix="/projects/{project_id}/tasks", tags=["Tasks"])
