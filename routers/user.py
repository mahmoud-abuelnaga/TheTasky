# external modules
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

# our modules
from schemas import user as userSchemas, team as teamSchemas
from utils import database, user as userUtils, auth
from models.user import UserModel

# setup
router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.delete("/me")
def deleteUser(
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> dict[str, str]:
    userUtils.deleteUser(reqUser, db)
    return {"message": "User Deleted"}


@router.patch("/me")
def updateUser(
    updateData: userSchemas.UserUpdate,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> userSchemas.UserRead:
    return userUtils.updateUser(reqUser, updateData, db)



@router.get("/me/teams")
def getTeams(
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> list[teamSchemas.TeamRead]:
    teams = reqUser.joinedTeams
    teams.extend(reqUser.createdTeams)
    return teams


@router.get("/{userID}")
def getUser(
    userID: int,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> userSchemas.UserRead:
    user = userUtils.getUser(userID, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
