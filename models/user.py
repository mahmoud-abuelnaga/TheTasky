# external modules
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
import re

# our modules
from models.task import TaskModel
from utils import database
from models.teamMembers import associationTable
from utils import hashing

# Helpers
Base = database.getBase()


# Definition
class UserModel(Base):
    __tablename__ = "users"

    # attributes
    __id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __name: Mapped[str] = mapped_column("name", String(20), nullable=False)
    __email: Mapped[str] = mapped_column(
        "email", String(40), unique=True, index=True, nullable=False
    )
    __password: Mapped[str] = mapped_column("password", String(120), nullable=False)

    # relations
    assignedTasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="assignedTo", foreign_keys=[TaskModel.assignedToID]
    )
    createdTasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="creator", foreign_keys=[TaskModel.creatorID],
        cascade="all, delete-orphan"
    )
    createdTeams: Mapped[list["TeamModel"]] = relationship(back_populates="teamCreator", cascade="all, delete-orphan")
    joinedTeams: Mapped[list["TeamModel"]] = relationship(
        back_populates="members", secondary=associationTable
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

        if len(value) > 20:
            raise Exception("Max length for name is 20")

        self.__name = value

    @hybrid_property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value: str):  # come back and verify
        self.__email = value

    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value: str):
        if value is None or value == "" or len(value) < 5 or len(value) > 20:
            raise Exception("Password needs to be at least of length 5 and max of 20")

        if bool(re.search(r"\s", value)):
            raise Exception("Password can't have spaces in it")

        self.__password = hashing.hash(value)
