from abc import ABC, abstractmethod
from typing import List
from app.models.project import Project
from app.models.task import Task, TaskStatus
from datetime import datetime

class ProjectRepository(ABC):
    @abstractmethod
    def create(self, name: str, description: str | None = None) -> Project: ...

    @abstractmethod
    def get(self, project_id: int) -> Project: ...

    @abstractmethod
    def update(self, project: Project) -> Project: ...

    @abstractmethod
    def delete(self, project_id: int) -> None: ...

    @abstractmethod
    def list_all(self) -> List[Project]: ...

class TaskRepository(ABC):
    @abstractmethod
    def create(self, project: Project, title: str, description: str | None = None,
               status: TaskStatus = TaskStatus.TODO, deadline: datetime | None = None) -> Task: ...

    @abstractmethod
    def get(self, task_id: int) -> Task: ...

    @abstractmethod
    def update(self, task: Task) -> Task: ...

    @abstractmethod
    def delete(self, task_id: int) -> None: ...

    @abstractmethod
    def list_by_project(self, project: Project) -> List[Task]: ...

    @abstractmethod
    def get_overdue_tasks(self) -> List[Task]: ...
