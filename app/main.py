from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routers import api_router
from app.exceptions.base import TodoListError

# Create the FastAPI application
app = FastAPI(
    title="ToDoList API",
    description="A complete Web API for managing projects and tasks.",
    version="3.0.0"
)

# Add a custom exception handler for all TodoListError subclasses
@app.exception_handler(TodoListError)
async def todolist_exception_handler(request: Request, exc: TodoListError):
    """
    Handles all custom application errors and returns a standardized
    JSON response.
    """
    # Default to 400 Bad Request, but can be customized per exception type
    status_code = 400
    if "not found" in str(exc).lower():
        status_code = 404
    elif "limit exceeded" in str(exc).lower():
        status_code = 409  # Conflict or 422
    elif "duplicate" in str(exc).lower():
        status_code = 409  # Conflict

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "type": type(exc).__name__,
                "message": str(exc)
            }
        },
    )


# Include the main API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint providing basic information about the API.
    """
    return {
        "message": "Welcome to the ToDoList API!",
        "documentation": "/docs"
    }
