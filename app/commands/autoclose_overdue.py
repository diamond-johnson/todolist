import asyncio
from datetime import datetime
from app.db.session import AsyncSessionLocal
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.models.task import TaskStatus

async def autoclose_overdue_tasks() -> None:
    """
    The core logic to find and close overdue tasks, now called directly
    by the async-native scheduler.
    """
    print("Running auto-close for overdue tasks...")
    async with AsyncSessionLocal() as db:
        repo = SQLAlchemyTaskRepository(db)
        overdue_tasks = await repo.get_overdue_tasks()
        if not overdue_tasks:
            print("No overdue tasks to close.")
            return

        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = datetime.utcnow()

        await db.commit()
        print(f"Closed {len(overdue_tasks)} overdue tasks.")


if __name__ == "__main__":
    asyncio.run(autoclose_overdue_tasks())
