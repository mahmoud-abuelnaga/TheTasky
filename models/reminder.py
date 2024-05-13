# external modules
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

# our modules
from utils import database

# Helpers
Base = database.getBase()


# Definition
class ReminderModel(Base):
    __tablename__ = "reminders"

    # attributes
    __id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __time: Mapped[datetime] = mapped_column("time", nullable=False)

    ## relations
    __taskID: Mapped[int] = mapped_column(
        "taskID",
        ForeignKey("tasks.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    task: Mapped["TaskModel"] = relationship(back_populates="reminders")

    # properties
    @hybrid_property
    def id(self):
        return self.__id

    @hybrid_property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value: datetime):
        if value is None:
            raise Exception("Time can't be none")

        if type(value) is not datetime:
            raise Exception("Need to pass a datetime object")

        self.__time = value

    @hybrid_property
    def taskID(self):
        return self.__taskID

    @taskID.setter
    def taskID(self, value: int):
        if value is None:
            raise Exception("Task ID can't be none")

        if type(value) is not int:
            raise Exception("Need to pass an integer")

        if self.taskID:
            raise Exception("Can't change the task after you set it")

        self.__taskID = value
