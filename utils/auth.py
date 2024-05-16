# external modules
import subprocess
from jose import jwt
from datetime import timedelta, timezone, datetime
from fastapi import Request, HTTPException, status, Depends, Header
from utils import user as userUtils, database
from sqlalchemy.orm import Session
from typing import Annotated

# Models
from models.user import UserModel
from models.task import TaskModel
from models.team import TeamModel

# constants
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
CMD = ["openssl", "rand", "-hex", "32"]
# SECRET_KEY = subprocess.check_output(CMD, stderr=subprocess.STDOUT).decode('utf-8')
SECRET_KEY = "HS256"


# Definition
def createAccessToken(data: dict):
    data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def decodeToken(token: str) -> str | None:
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # decode
    except:
        return None

    # get id and email
    id: int = payload.get("id")
    email: str = payload.get("email")

    # if they don't exist, something went wrong with the token
    if id is None or email is None:
        return None

    return email


async def getRequestUser(
    token_bearer: Annotated[str, Header()], db: Session = Depends(database.getSession)
):
    token = token_bearer
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    email = await decodeToken(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    user = userUtils.getUser(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return user


def isMemberInTeam(user: UserModel, team: TeamModel):
    try:
        inTeam = team.members.index(user)
    except Exception as e:
        return False

    return True


def canAccessTask(user: UserModel, task: TaskModel):
    if (
        not isMemberInTeam(user, task.assignedTeam) and task.creatorID != user.id
    ):  # TODO: CHECK if the condition works for teams
        return False
    else:
        return True
