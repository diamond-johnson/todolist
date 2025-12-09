import schedule
import time
from .autoclose_overdue import autoclose_overdue_tasks

def start_scheduler():
    schedule.every(15).minutes.do(autoclose_overdue_tasks)
    print("Scheduler started – checking overdue tasks every 15 minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()