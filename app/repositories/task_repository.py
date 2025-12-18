from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.exceptions.repository_exceptions import TaskNotFoundError
from typing import List, Any
from datetime import datetime
from . import TaskRepository
from typing import cast, List
from sqlalchemy import select

class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project, title: str, description: str | None = None,
               status: TaskStatus = TaskStatus.TODO, deadline: datetime | None = None) -> Task:
        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project.id
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, task_id: int) -> Task:
        stmt = select(Task).where(Task.id == task_id)
        task = self.db.execute(stmt).scalar_one_or_none()
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    def update(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        task = self.get(task_id)
        self.db.delete(task)
        self.db.commit()

    def list_by_project(self, project: Project) -> List[Task]:
        stmt = select(Task).where(Task.project_id == project.id).order_by(Task.created_at)
        return list(self.db.execute(stmt).scalars().all())

    def get_overdue_tasks(self) -> List[Task]:
        now = datetime.utcnow()
        stmt = select(Task).where(Task.deadline < now, Task.status != TaskStatus.DONE)
        return list(self.db.execute(stmt).scalars().all())
