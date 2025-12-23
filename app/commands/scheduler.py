import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.commands.autoclose_overdue import autoclose_overdue_tasks
from app.db.session import SYNC_DATABASE_URL


async def start_scheduler() -> None:
    """
    Start the persistent, asynchronous scheduler for auto-closing overdue tasks.
    """

    scheduler = AsyncIOScheduler(
        jobstores={
            'default': SQLAlchemyJobStore(url=SYNC_DATABASE_URL)
        }
    )

    scheduler.add_job(
        autoclose_overdue_tasks,
        'interval',
        minutes=1,
        id='autoclose_overdue',
        replace_existing=True
    )

    scheduler.start()
    print("Async scheduler started – auto-closing overdue tasks every 1 minute.")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler shutting down...")
        scheduler.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(start_scheduler())
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
