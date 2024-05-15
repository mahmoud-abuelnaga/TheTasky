from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from schemas import remainder
from models.reminder import ReminderModel

scheduler = BackgroundScheduler()

def get_remainders(db: Session, due_time: datetime):
    return db.query(ReminderModel).filter(ReminderModel.time <= due_time).all()


def check_reminders_due():
    now = datetime.now()
    due_time = now + timedelta(minutes=2)
    
    due_reminders = get_remainders(due_time)
    
    for reminder in due_reminders:
        send_notification(reminder)

def start_scheduler():
    scheduler.add_job(
        check_reminders_due,
        trigger=IntervalTrigger(hours=12),
        id="check_reminders_job",
        name="Check Reminders Due",
        replace_existing=True
    )
    scheduler.start()

def send_notification(reminder: remainder.Reminder):
    
    print(f"Sending notification for reminder: {reminder}")
    
