# app/repositories/task_repository.py
from typing import Protocol, List
from app.models.task import Task, TaskId
from app.models.project import Project
from app.exceptions.repository_exceptions import TaskNotFoundError


class TaskRepositoryProtocol(Protocol):
    def get_next_task_id(self) -> TaskId: ...
    def add_task(self, project: Project, task: Task) -> None: ...
    def get_tasks(self, project: Project) -> List[Task]: ...
    def get_task(self, project: Project, task_id: TaskId) -> Task: ...
    def update_task(self, project: Project, task: Task) -> None: ...
    def delete_task(self, project: Project, task_id: TaskId) -> None: ...


class InMemoryTaskRepository:
    """In-memory repository for tasks (attached to projects)."""

    def __init__(self) -> None:
        self._next_task_id: int = 1

    def get_next_task_id(self) -> TaskId:
        tid = TaskId(self._next_task_id)
        self._next_task_id += 1
        return tid

    def add_task(self, project: Project, task: Task) -> None:
        project.tasks.append(task)

    def get_tasks(self, project: Project) -> List[Task]:
        return sorted(project.tasks, key=lambda t: t.created_at)

    def get_task(self, project: Project, task_id: TaskId) -> Task:
        for task in project.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    def update_task(self, project: Project, task: Task) -> None:
        for idx, existing in enumerate(project.tasks):
            if existing.id == task.id:
                project.tasks[idx] = task
                return
        raise TaskNotFoundError(f"Task with ID {task.id} not found")

    def delete_task(self, project: Project, task_id: TaskId) -> None:
        for idx, task in enumerate(project.tasks):
            if task.id == task_id:
                del project.tasks[idx]
                return
        raise TaskNotFoundError(f"Task with ID {task_id} not found")