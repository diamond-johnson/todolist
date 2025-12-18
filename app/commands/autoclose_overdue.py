from datetime import datetime
from app.db.session import SessionLocal
from app.repositories.task_repository import SQLAlchemyTaskRepository
from app.models.task import TaskStatus

def autoclose_overdue_tasks() -> None:
    """Close overdue tasks automatically to enforce deadlines (runs as scheduled command)."""
    with SessionLocal() as db:
        repo = SQLAlchemyTaskRepository(db)
        overdue = repo.get_overdue_tasks()
        for task in overdue:
            task.status = TaskStatus.DONE
            task.closed_at = datetime.utcnow()
        db.commit()
        print(f"Closed {len(overdue)} overdue tasks.")

if __name__ == "__main__":
    autoclose_overdue_tasks()