# external modules
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional

# our modules



class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    email: EmailStr


class UserSignup(UserBase):
    password: str = Field(min_length=5, max_length=20)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=20)]] = None
    email: EmailStr | None = None
    password: Optional[Annotated[str, Field(min_length=5, max_length=20)]] = None

