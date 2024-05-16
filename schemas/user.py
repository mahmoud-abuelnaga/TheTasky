# external modules
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional

# our modules
from schemas import task, team


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    email: EmailStr


class UserSignup(UserBase):
    password: str = Field(min_length=5, max_length=20)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class DetailedUserRead(UserBase):
    createdTeams: list[team.TeamRead]
    joinedTeams: list[team.TeamRead]
    createdTasks: list[task.TaskRead]
    assignedTasks: list[task.TaskRead]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=20)]] = None
    email: EmailStr | None = None
    password: Optional[Annotated[str, Field(min_length=5, max_length=20)]] = None


class UserDetailed(BaseModel):
    id: int
    name: str
    email: EmailStr
    tasks: list[task.TaskRead]
    teams: list[team.TeamRead]

    class Config:
        from_attributes = True
