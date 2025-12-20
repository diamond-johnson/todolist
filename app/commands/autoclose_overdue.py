import asyncio
from datetime import datetime
from app.db.session import AsyncSessionLocal
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.models.task import TaskStatus


async def _autoclose_logic():
    """The core logic, now running asynchronously."""
    async with AsyncSessionLocal() as db:
        repo = SQLAlchemyTaskRepository(db)
        # We must 'await' the async method
        overdue_tasks = await repo.get_overdue_tasks()
        if not overdue_tasks:
            print("No overdue tasks to close.")
            return

        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = datetime.utcnow()

        await db.commit()
        print(f"Closed {len(overdue_tasks)} overdue tasks.")


def autoclose_overdue_tasks() -> None:
    """
    Synchronous wrapper that runs the async logic.
    This is what the scheduler will call.
    """
    print("Running auto-close for overdue tasks...")
    asyncio.run(_autoclose_logic())


if __name__ == "__main__":
    autoclose_overdue_tasks()
