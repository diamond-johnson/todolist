import sys
import warnings
from typing import NoReturn, Optional
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.project import Project
from app.models.task import Task, TaskStatus
from app.repositories.project_repository import SQLAlchemyProjectRepository
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.db.session import SessionLocal  # This will be the synchronous session for the CLI
from app.core.config import Config
from app.exceptions.base import TodoListError, ValidationError
from datetime import datetime

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
    """Get user input, allowing optional fields (for flexibility in CLI)."""
    value = input(prompt).strip()
    if optional and not value:
        return None
    if not value and not optional:
        # We can make the prompt a bit more specific for the error message
        field_name = prompt.split(":")[0]
        raise ValueError(f"{field_name} is required")
    return value

class CLI:
    """
    Command Line Interface for interacting with To-Do List (main user entry point).
    This interface is deprecated and will be removed in a future version.
    """

    def __init__(self, config: Config):
        self.config = config

    def run(self) -> NoReturn:
        """Run the CLI loop, handling user choices and DB sessions (ensures isolation per action)."""
        warnings.warn(
            "The CLI is deprecated and will be removed in a future version. Please use the Web API.",
            DeprecationWarning
        )
        print("\nWARNING: The Command Line Interface (CLI) is deprecated and will be removed soon. Please migrate to the API.")

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
            choice = input("Enter choice: ").strip()

            if choice == "10":
                print("Exiting deprecated CLI.")
                sys.exit(0)

            # NOTE: The CLI must use a synchronous session. The new async session
            # is only for the FastAPI part of the application.
            # We assume SessionLocal can still be instantiated synchronously.
            # If your new session.py *only* has async, this part needs adjustment.
            # However, the provided session.py for phase 2 should work fine.
            try:
                with SessionLocal() as db:
                    project_repo = SQLAlchemyProjectRepository(db)
                    task_repo = SQLAlchemyTaskRepository(db)
                    project_service = ProjectService(project_repo, self.config)
                    task_service = TaskService(project_repo, task_repo, self.config)

                    if choice == "1":
                        name = get_input("Project name: ")
                        desc = get_input("Project description (optional): ", optional=True)
                        project = project_service.create_project(name, desc)
                        print("Project created:")
                        print_project(project)

                    elif choice == "2":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        new_name = get_input("New name (blank to skip): ", optional=True)
                        new_desc = get_input("New description (blank to skip): ", optional=True)
                        if new_name is None and new_desc is None:
                            print("No changes made.")
                            continue
                        project = project_service.edit_project(pid, new_name, new_desc)
                        print("Project updated:")
                        print_project(project)

                    elif choice == "3":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        project_service.delete_project(pid)
                        print("Project deleted successfully.")

                    elif choice == "4":
                        projects = project_service.list_projects()
                        if not projects:
                            print("No projects exist.")
                        for project in projects:
                            print_project(project)

                    elif choice == "5":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        title = get_input("Task title: ")
                        desc = get_input("Task description (optional): ", optional=True)
                        status_input = get_input("Status (todo/doing/done, default todo): ", optional=True) or "todo"
                        deadline = get_input("Deadline (YYYY-MM-DD, blank for none): ", optional=True)
                        task = task_service.create_task(pid, title, desc, status_input, deadline)
                        print("Task created:")
                        print_task(task)

                    elif choice == "6":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        tid_str = get_input("Task ID: ")
                        tid = int(tid_str)
                        new_status = get_input("New status (todo/doing/done): ")
                        task = task_service.change_task_status(pid, tid, new_status)
                        print("Task status updated:")
                        print_task(task)

                    elif choice == "7":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        tid_str = get_input("Task ID: ")
                        tid = int(tid_str)
                        new_title = get_input("New title (blank to skip): ", optional=True)
                        new_desc = get_input("New description (blank to skip): ", optional=True)
                        new_status = get_input("New status (todo/doing/done, blank to skip): ", optional=True)
                        new_deadline = get_input("New deadline (YYYY-MM-DD, blank to skip): ", optional=True)
                        if all(x is None for x in [new_title, new_desc, new_status, new_deadline]):
                            print("No changes made.")
                            continue
                        task = task_service.edit_task(pid, tid, new_title, new_desc, new_status, new_deadline)
                        print("Task updated:")
                        print_task(task)

                    elif choice == "8":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        tid_str = get_input("Task ID: ")
                        tid = int(tid_str)
                        task_service.delete_task(pid, tid)
                        print("Task deleted successfully.")

                    elif choice == "9":
                        pid_str = get_input("Project ID: ")
                        pid = int(pid_str)
                        tasks = task_service.list_tasks(pid)
                        if not tasks:
                            print("No tasks in this project.")
                        for task in tasks:
                            print_task(task)

                    else:
                        print("Invalid choice. Try again.")

            except (TodoListError, ValueError, TypeError) as e:
                # Catching TypeError as well for int() conversion failures
                print(f"Error: {e}")
