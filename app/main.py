from app.cli.console import CLI
from app.core.config import Config
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.db.session import SessionLocal

def main() -> None:
    config = Config()

    cli = CLI(None, None)  # Placeholder, we'll inject per operation
    cli.run()  # But override run below if needed, or modify CLI class

# Instead, since CLI.run is the loop, we need to adjust CLI to handle DB per op.
# Update CLI class in console.py or here; for simplicity, move logic to main loop.

# Better: Replace main with a loop here, using CLI functions, but to keep DI, let's assume we modify CLI.run to accept config and create repos inside.

# Alternative: Update console.py CLI.run as below (move this logic there if preferred).

# For now, I'll provide a combined main with loop for Phase 2.

import sys
from typing import NoReturn
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.project import Project
from app.models.task import Task
from app.exceptions.base import TodoListError, ValidationError
from app.db.session import SessionLocal
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.core.config import Config

def print_project(project: Project) -> None:
    """Print project details."""
    print(
        f"ID: {project.id}, Name: {project.name}, "
        f"Description: {project.description or 'None'}, "
        f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )

def print_task(task: Task) -> None:
    """Print task details."""
    deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "None"
    print(
        f"ID: {task.id}, Title: {task.title}, Status: {task.status}, "
        f"Deadline: {deadline_str}, "
        f"Description: {task.description or 'None'}, "
        f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )

def get_input(prompt: str, optional: bool = False) -> str | None:
    """Get user input, allowing blank for optional fields."""
    value = input(prompt).strip()
    if optional and not value:
        return None
    if not value and not optional:
        raise ValueError(f"{prompt.strip()} is required")
    return value

def cli_loop(config: Config) -> NoReturn:
    while True:
        print("\nTo-Do List Menu:")
        print("1. Create Project")
        # ... (same menu as in console.py)
        choice = input("Enter choice: ").strip()

        if choice == "10":
            sys.exit(0)

        with SessionLocal() as db:
            project_repo = SQLAlchemyProjectRepository(db)
            task_repo = SQLAlchemyTaskRepository(db)
            project_service = ProjectService(project_repo, config)
            task_service = TaskService(project_repo, task_repo, config)

            try:
                if choice == "1":
                    name = get_input("Project name: ")
                    desc = get_input("Project description (optional): ", optional=True)
                    project = project_service.create_project(name, desc)
                    print("Project created:")
                    print_project(project)
                # ... (copy the rest of the if-elif from console.py CLI.run, replacing self.project_service -> project_service, etc.)
                # For brevity, assume you copy-paste the logic from your console.py here.
                else:
                    print("Invalid choice. Try again.")
            except TodoListError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Invalid input: {e}")

if __name__ == "__main__":
    config = Config()
    cli_loop(config)