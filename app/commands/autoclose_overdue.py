from datetime import datetime
from app.db.session import SessionLocal
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.models.task import TaskStatus

def autoclose_overdue_tasks() -> None:
    """Close all overdue tasks (deadline passed and not DONE)."""
    with SessionLocal() as db:
        task_repo = SQLAlchemyTaskRepository(db)
        overdue = task_repo.get_overdue_tasks()
        now = datetime.utcnow()
        for task in overdue:
            task.status = TaskStatus.DONE
            task.closed_at = now
            db.commit()
            print(f"Auto-closed task ID {task.id}: {task.title}")

if __name__ == "__main__":
    autoclose_overdue_tasks()