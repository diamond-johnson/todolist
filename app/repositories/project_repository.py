# app/repositories/project_repository.py
from typing import Protocol, List
from app.models.project import Project, ProjectId
from app.exceptions.repository_exceptions import ProjectNotFoundError


class ProjectRepositoryProtocol(Protocol):
    def get_next_project_id(self) -> ProjectId: ...
    def add_project(self, project: Project) -> None: ...
    def get_projects(self) -> List[Project]: ...
    def get_project(self, project_id: ProjectId) -> Project: ...
    def update_project(self, project: Project) -> None: ...
    def delete_project(self, project_id: ProjectId) -> None: ...


class InMemoryProjectRepository:
    """In-memory repository for projects."""

    def __init__(self) -> None:
        self._projects: dict[ProjectId, Project] = {}
        self._next_project_id: int = 1

    def get_next_project_id(self) -> ProjectId:
        pid = ProjectId(self._next_project_id)
        self._next_project_id += 1
        return pid

    def add_project(self, project: Project) -> None:
        self._projects[project.id] = project

    def get_projects(self) -> List[Project]:
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