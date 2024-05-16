# external modules
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import re

# our modules
from utils import database
from models.reminder import ReminderModel

# Helpers
Base = database.getBase()


class TaskModel(Base):
    __tablename__ = "tasks"

    # attributes
    __id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __name: Mapped[str] = mapped_column("name", String(120), nullable=False)
    __createdAt: Mapped[datetime] = mapped_column(
        "createdAt", nullable=False, default=datetime.now()
    )
    __priority: Mapped[int] = mapped_column("priority", nullable=False, default=5)
    __status: Mapped[str] = mapped_column(
        "status", String(13), nullable=False, default="not started"
    )
    __progress: Mapped[int] = mapped_column("progress", nullable=False, default=0)
    __deadline: Mapped[datetime] = mapped_column("deadline", nullable=True)

    ## relations
    __assignedToID: Mapped[int] = mapped_column(
        "assignedToID",
        ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    assignedTo: Mapped["UserModel"] = relationship(
        back_populates="assignedTasks", foreign_keys=[__assignedToID]
    )

    __creatorID: Mapped[int] = mapped_column(
        "creatorID",
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    creator: Mapped["UserModel"] = relationship(
        back_populates="createdTasks", foreign_keys=[__creatorID]
    )

    __teamID: Mapped[int] = mapped_column(
        "teamID",
        ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )
    assignedTeam: Mapped["TeamModel"] = relationship(back_populates="assignedTasks")

    __parentTaskID: Mapped[int] = mapped_column(
        "parentTaskID",
        ForeignKey("tasks.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    parentTask: Mapped["TaskModel"] = relationship(
        backref="subTasks", remote_side="TaskModel.id"
    )

    reminders: Mapped[list["ReminderModel"]] = relationship(back_populates="task", cascade="all, delete-orphan")

    # properties
    @hybrid_property
    def id(self):
        return self.__id

    @hybrid_property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        value = value.strip()
        if value is None or value == "" or len(value) < 2:
            raise Exception("Name needs to be at least of length 2")

        self.__name = value

    @hybrid_property
    def createdAt(self):
        return self.__createdAt

    @hybrid_property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value: int):
        if value is None:
            value = 5

        if value < 1 or value > 5:
            raise Exception("Priority needs to be between 1 and 5 inclusive")

        self.__priority = value

    @hybrid_property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str):
        if value is None:
            raise Exception("Status can't be none")

        self.__status = value

    @hybrid_property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, value: int):
        if value is None:
            raise Exception("Progress can't be none")

        if value < 0 or value > 100:
            raise Exception("Progress needs to be between 0 and 100 inclusive")

        self.__progress = value

    @hybrid_property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, value: datetime):
        self.__deadline = value

    @hybrid_property
    def assignedToID(self):
        return self.__assignedToID

    @assignedToID.setter
    def assignedToID(self, value: int):
        self.__assignedToID = value

    @hybrid_property
    def creatorID(self):
        return self.__creatorID

    @creatorID.setter
    def creatorID(self, value: int):
        if self.creatorID:
            raise Exception("Can't change creator")

        if value is None:
            raise Exception("Creator can't be none")

        self.__creatorID = value

    @hybrid_property
    def teamID(self):
        return self.__teamID

    @teamID.setter
    def teamID(self, value: int):
        if self.teamID:
            raise Exception("Can't change team")

        if value is None and self.teamID:
            raise Exception("Can't change team to none")

        self.__teamID = value

    @hybrid_property
    def parentTaskID(self):
        return self.__parentTaskID

    @parentTaskID.setter
    def parentTaskID(self, value: int):
        self.__parentTaskID = value
