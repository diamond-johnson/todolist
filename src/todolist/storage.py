from typing import Protocol

from .models import Project, Task, ProjectId, TaskId

from .exceptions import ProjectNotFoundError, TaskNotFoundError


class Storage(Protocol):
    """Protocol for storage operations."""

    def get_next_project_id(self) -> ProjectId: ...

    def get_next_task_id(self) -> TaskId: ...

    def add_project(self, project: Project) -> None: ...

    def get_projects(self) -> list[Project]: ...

    def get_project(self, project_id: ProjectId) -> Project: ...

    def update_project(self, project: Project) -> None: ...

    def delete_project(self, project_id: ProjectId) -> None: ...

    def add_task(self, project_id: ProjectId, task: Task) -> None: ...

    def get_tasks(self, project_id: ProjectId) -> list[Task]: ...

    def get_task(self, project_id: ProjectId, task_id: TaskId) -> Task: ...

    def update_task(self, project_id: ProjectId, task: Task) -> None: ...

    def delete_task(self, project_id: ProjectId, task_id: TaskId) -> None: ...


class InMemoryStorage:
    """In-memory implementation of Storage."""

    def __init__(self) -> None:
        self._projects: dict[ProjectId, Project] = {}
        self._next_project_id: int = 1
        self._next_task_id: int = 1

    def get_next_project_id(self) -> ProjectId:
        pid = ProjectId(self._next_project_id)
        self._next_project_id += 1
        return pid

    def get_next_task_id(self) -> TaskId:
        tid = TaskId(self._next_task_id)
        self._next_task_id += 1
        return tid

    def add_project(self, project: Project) -> None:
        self._projects[project.id] = project

    def get_projects(self) -> list[Project]:
        return sorted(self._projects.values(), key=lambda p: p.created_at)

    def get_project(self, project_id: ProjectId) -> Project:
        try:
            return self._projects[project_id]
        except KeyError:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

    def update_project(self, project: Project) -> None:
        if project.id not in self._projects:
            raise ProjectNotFoundError(f"Project with ID {project.id} not found")
        self._projects[project.id] = project

    def delete_project(self, project_id: ProjectId) -> None:
        if project_id not in self._projects:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        del self._projects[project_id]

    def add_task(self, project_id: ProjectId, task: Task) -> None:
        project = self.get_project(project_id)
        project.tasks.append(task)

    def get_tasks(self, project_id: ProjectId) -> list[Task]:
        project = self.get_project(project_id)
        return sorted(project.tasks, key=lambda t: t.created_at)

    def get_task(self, project_id: ProjectId, task_id: TaskId) -> Task:
        project = self.get_project(project_id)
        for task in project.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}")

    def update_task(self, project_id: ProjectId, task: Task) -> None:
        project = self.get_project(project_id)
        for idx, existing_task in enumerate(project.tasks):
            if existing_task.id == task.id:
                project.tasks[idx] = task
                return
        raise TaskNotFoundError(f"Task with ID {task.id} not found in project {project_id}")

    def delete_task(self, project_id: ProjectId, task_id: TaskId) -> None:
        project = self.get_project(project_id)
        for idx, task in enumerate(project.tasks):
            if task.id == task_id:
                del project.tasks[idx]
                return
        raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}")