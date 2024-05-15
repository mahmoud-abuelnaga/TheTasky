from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ReminderBase(BaseModel):
    time: datetime
    taskID : int

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
