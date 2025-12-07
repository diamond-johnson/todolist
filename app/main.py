# app/main.py
from app.cli.console import CLI
from app.core.config import Config
from app.repositories.project_repository import InMemoryProjectRepository
from app.repositories.task_repository import InMemoryTaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def main() -> None:
    config = Config()
    project_repo = InMemoryProjectRepository()
    task_repo = InMemoryTaskRepository()

    project_service = ProjectService(project_repo, task_repo, config)
    task_service = TaskService(project_repo, task_repo, config)

    cli = CLI(project_service, task_service)
    cli.run()


if __name__ == "__main__":
    main()