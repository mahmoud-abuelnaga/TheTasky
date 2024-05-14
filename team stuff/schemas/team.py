# external modules
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, Annotated


# defintions
class TeamBase(BaseModel):
    name: str = Field(min_length=2, max_length=20)


class TeamRead(TeamBase):
    id: int
    createdAt: datetime
    creatorID: int

    class Config:
        from_attributes = True


class TeamCreate(TeamBase):
    pass


class AddMember(BaseModel):
    email: EmailStr


class UpdateTeam(BaseModel):
    name: Optional[Annotated[str, Field(min_length=2, max_length=20)]] = None


class RemoveMember(BaseModel):
    memberID: int
