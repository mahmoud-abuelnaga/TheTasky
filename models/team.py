# external modules
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import re

# our modules
from utils import database
from models.teamMembers import associationTable

# Helpers
Base = database.getBase()

# definitions


class TeamModel(Base):
    __tablename__ = "teams"
    # attributes
    __id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __name: Mapped[str] = mapped_column("name", String(20), nullable=False)
    __createdAt: Mapped[datetime] = mapped_column(
        "createdAt", nullable=False, default=datetime.now()
    )

    # relations
    __creatorID: Mapped[int] = mapped_column(
        "creatorID",
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    teamCreator: Mapped["UserModel"] = relationship(back_populates="createdTeams")

    assignedTasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="assignedTeam"
    )
    members: Mapped[list["UserModel"]] = relationship(
        back_populates="joinedTeams", secondary=associationTable
    )

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
    def creatorID(self):
        return self.__creatorID

    @creatorID.setter
    def creatorID(self, value: int):
        if self.creatorID:
            raise Exception("Can't change creator")

        if value is None:
            raise Exception("Creator can't be none")

        self.__creatorID = value
