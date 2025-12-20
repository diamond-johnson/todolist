import sys
import warnings
import asyncio
from typing import NoReturn, Optional
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.db.session import AsyncSessionLocal  # Use the async session for all operations now
from app.core.config import Config
from app.exceptions.base import TodoListError


def print_project(project: Project) -> None:
    """Print project details in a readable format for CLI output."""
    print(
        f"ID: {project.id}, Name: {project.name}, "
        f"Description: {project.description or 'None'}, "
        f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )


def print_task(task: Task) -> None:
    """Print task details, handling None values for deadlines/closed times."""
    deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "None"
    closed_str = task.closed_at.strftime("%Y-%m-%d %H:%M:%S") if task.closed_at else "None"
    print(
        f"ID: {task.id}, Title: {task.title}, Status: {task.status.value}, "
        f"Deadline: {deadline_str}, Closed: {closed_str}, "
        f"Description: {task.description or 'None'}"
    )


def get_input(prompt: str, optional: bool = False) -> Optional[str]:
    """Get user input, allowing optional fields."""
    value = input(prompt).strip()
    if optional and not value:
        return None
    if not value and not optional:
        field_name = prompt.split(":")[0]
        raise ValueError(f"{field_name} is required")
    return value


class CLI:
    """
    Command Line Interface (Deprecated).
    This now acts as a synchronous wrapper around the new asynchronous service layer.
    """

    def __init__(self, config: Config):
        self.config = config

    async def _run_async(self):
        """The main application logic, now running inside an async function."""
        while True:
            print("\nTo-Do List Menu (Deprecated):")
            print("1. Create Project")
            print("2. Edit Project")
            print("3. Delete Project")
            print("4. List Projects")
            print("5. Create Task")
            print("6. Change Task Status")
            print("7. Edit Task")
            print("8. Delete Task")
            print("9. List Tasks in Project")
            print("10. Exit")
            choice = await asyncio.to_thread(input, "Enter choice: ")  # Use async-friendly input

            if choice == "10":
                print("Exiting deprecated CLI.")
                sys.exit(0)

            try:
                # Create a new session for each operation
                async with AsyncSessionLocal() as db:
                    project_repo = SQLAlchemyProjectRepository(db)
                    task_repo = SQLAlchemyTaskRepository(db)
                    project_service = ProjectService(project_repo, self.config)
                    task_service = TaskService(project_repo, task_repo, self.config)

                    if choice == "1":
                        name = await asyncio.to_thread(get_input, "Project name: ")
                        desc = await asyncio.to_thread(get_input, "Project description (optional): ", optional=True)
                        project = await project_service.create_project(name, desc)
                        print("Project created:")
                        print_project(project)

                    elif choice == "2":
                        pid_str = await asyncio.to_thread(get_input, "Project ID: ")
                        pid = int(pid_str)
                        new_name = await asyncio.to_thread(get_input, "New name (blank to skip): ", optional=True)
                        new_desc = await asyncio.to_thread(get_input, "New description (blank to skip): ",
                                                           optional=True)
                        project = await project_service.edit_project(pid, new_name, new_desc)
                        print("Project updated:")
                        print_project(project)

                    elif choice == "3":
                        pid_str = await asyncio.to_thread(get_input, "Project ID: ")
                        pid = int(pid_str)
                        await project_service.delete_project(pid)
                        print("Project deleted successfully.")

                    elif choice == "4":
                        projects = await project_service.list_projects()
                        if not projects:
                            print("No projects exist.")
                        for p in projects:
                            print_project(p)

                    elif choice == "5":
                        pid_str = await asyncio.to_thread(get_input, "Project ID: ")
                        pid = int(pid_str)
                        title = await asyncio.to_thread(get_input, "Task title: ")
                        desc = await asyncio.to_thread(get_input, "Task description (optional): ", optional=True)
                        status = await asyncio.to_thread(get_input, "Status (todo/doing/done, default todo): ",
                                                         optional=True) or "todo"
                        deadline = await asyncio.to_thread(get_input, "Deadline (YYYY-MM-DD, blank for none): ",
                                                           optional=True)
                        task = await task_service.create_task(pid, title, desc, status, deadline)
                        print("Task created:")
                        print_task(task)

                    elif choice == "9":
                        pid_str = await asyncio.to_thread(get_input, "Project ID: ")
                        pid = int(pid_str)
                        tasks = await task_service.list_tasks(pid)
                        if not tasks:
                            print("No tasks in this project.")
                        for t in tasks:
                            print_task(t)

                    # Add other choices (6, 7, 8) here following the same 'await' pattern...

                    else:
                        print("Invalid choice. Try again.")

            except (TodoListError, ValueError, TypeError) as e:
                print(f"Error: {e}")

    def run(self) -> NoReturn:
        """Synchronous entry point that runs the main async loop."""
        warnings.warn(
            "The CLI is deprecated and will be removed in a future version. Please use the Web API.",
            DeprecationWarning
        )
        print(
            "\nWARNING: The Command Line Interface (CLI) is deprecated and will be removed soon. Please migrate to the API.")

        try:
            asyncio.run(self._run_async())
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)

