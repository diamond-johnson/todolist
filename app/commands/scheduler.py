from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.commands.autoclose_overdue import autoclose_overdue_tasks
from app.db.session import SYNC_DATABASE_URL
import time

def start_scheduler() -> None:
    """Start persistent scheduler for auto-closing overdue tasks (runs in background, jobs saved in DB)."""
    scheduler = BackgroundScheduler(
        jobstores={'default': SQLAlchemyJobStore(url=SYNC_DATABASE_URL)}
    )
    scheduler.add_job(autoclose_overdue_tasks, 'interval', minutes=15, id='autoclose_overdue')
    scheduler.start()
    print("Scheduler started – auto-closing overdue tasks every 15 minutes (persistent via DB).")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()
