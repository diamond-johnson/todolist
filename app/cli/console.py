import sys
from typing import NoReturn

from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.project import Project, ProjectId
from app.models.task import Task, TaskId
from app.exceptions.base import TodoListError, ValidationError

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


class CLI:
    """Main CLI application with injected dependencies."""

    def __init__(self, project_service: ProjectService, task_service: TaskService) -> None:
        self.project_service = project_service
        self.task_service = task_service

    def run(self) -> NoReturn:
        """Main CLI loop."""
        while True:
            print("\nTo-Do List Menu:")
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
                sys.exit(0)

            try:
                if choice == "1":
                    name = get_input("Project name: ")
                    desc = get_input("Project description (optional): ", optional=True)
                    project = self.project_service.create_project(name, desc or "")
                    print("Project created:")
                    print_project(project)

                elif choice == "2":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    new_name = get_input("New name (blank to skip): ", optional=True)
                    new_desc = get_input("New description (blank to skip): ", optional=True)
                    if new_name is None and new_desc is None:
                        print("No changes made.")
                        continue
                    project = self.project_service.edit_project(pid, new_name, new_desc)
                    print("Project updated:")
                    print_project(project)

                elif choice == "3":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    self.project_service.delete_project(pid)
                    print("Project deleted successfully.")

                elif choice == "4":
                    projects = self.project_service.list_projects()
                    if not projects:
                        print("No projects exist.")
                        continue
                    for project in projects:
                        print_project(project)

                elif choice == "5":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    title = get_input("Task title: ")
                    desc = get_input("Task description (optional): ", optional=True)
                    status_input = get_input("Status (todo/doing/done, default todo): ", optional=True) or "todo"
                    deadline = get_input("Deadline (YYYY-MM-DD, blank for none): ", optional=True)
                    task = self.task_service.create_task(pid, title, desc or "", status_input, deadline)
                    print("Task created:")
                    print_task(task)

                elif choice == "6":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    tid_int = int(get_input("Task ID: ") or "")
                    tid = TaskId(tid_int)
                    new_status = get_input("New status (todo/doing/done): ")
                    if new_status is None:
                        raise ValidationError("New status required")
                    task = self.task_service.change_task_status(pid, tid, new_status)
                    print("Task status updated:")
                    print_task(task)

                elif choice == "7":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    tid_int = int(get_input("Task ID: ") or "")
                    tid = TaskId(tid_int)
                    new_title = get_input("New title (blank to skip): ", optional=True)
                    new_desc = get_input("New description (blank to skip): ", optional=True)
                    new_status = get_input("New status (todo/doing/done, blank to skip): ", optional=True)
                    new_deadline = get_input("New deadline (YYYY-MM-DD, blank to skip): ", optional=True)
                    if all(x is None for x in [new_title, new_desc, new_status, new_deadline]):
                        print("No changes made.")
                        continue
                    task = self.task_service.edit_task(pid, tid, new_title, new_desc, new_status, new_deadline)
                    print("Task updated:")
                    print_task(task)

                elif choice == "8":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    tid_int = int(get_input("Task ID: ") or "")
                    tid = TaskId(tid_int)
                    self.task_service.delete_task(pid, tid)
                    print("Task deleted successfully.")

                elif choice == "9":
                    pid_int = int(get_input("Project ID: ") or "")
                    pid = ProjectId(pid_int)
                    tasks = self.task_service.list_tasks(pid)
                    if not tasks:
                        print("No tasks in this project.")
                        continue
                    for task in tasks:
                        print_task(task)

                else:
                    print("Invalid choice. Try again.")

            except TodoListError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Invalid input: {e}")

