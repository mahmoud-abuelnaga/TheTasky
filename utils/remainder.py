# external modules
from sqlalchemy.orm import Session

# our modules
from models.reminder import ReminderModel
from schemas.remainder import ReminderCreate, Reminder


def createRemainder(task: ReminderCreate, creatorID: int, db: Session) -> Reminder:
    task = ReminderModel(**task.model_dump(), creatorID=creatorID)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
