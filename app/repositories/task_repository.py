from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.exceptions.repository_exceptions import TaskNotFoundError
from typing import List
from datetime import datetime
from . import TaskRepository

class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: AsyncSession):
        """The repository now expects an AsyncSession."""
        self.db = db

    async def create(self, project: Project, title: str, description: str | None = None,
                     status: TaskStatus = TaskStatus.TODO, deadline: datetime | None = None) -> Task:
        """Asynchronously creates a new task."""
        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project.id
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get(self, task_id: int) -> Task:
        """Asynchronously retrieves a task by its ID."""
        stmt = select(Task).where(Task.id == task_id)
        result = await self.db.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    async def update(self, task: Task) -> Task:
        """Asynchronously commits changes to a task."""
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task_id: int) -> None:
        """Asynchronously deletes a task."""
        task = await self.get(task_id) # Must await the get method
        await self.db.delete(task)
        await self.db.commit()

    async def list_by_project(self, project: Project) -> List[Task]:
        """Asynchronously lists all tasks for a given project."""
        stmt = select(Task).where(Task.project_id == project.id).order_by(Task.created_at)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_overdue_tasks(self) -> List[Task]:
        """Asynchronously gets all tasks that are past their deadline and not done."""
        now = datetime.utcnow()
        stmt = select(Task).where(Task.deadline < now, Task.status != TaskStatus.DONE)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
