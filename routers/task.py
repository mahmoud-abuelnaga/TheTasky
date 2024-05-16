# external modules
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

# our modules
from utils import database, task as taskUtils, auth
from schemas.task import TaskRead, TaskCreate, TaskUpdate
from models.user import UserModel

# setup
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/create")
def createTask(
    task: TaskCreate,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> TaskRead:
    try:
        task = taskUtils.createTask(task, reqUser.id, db)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return task


@router.get("/{taskID}")
def getTask(
    taskID: int,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> TaskRead:
    task = taskUtils.getTask(taskID, db)
    if not task:
        raise HTTPException(status_code=404, detail="Not Found!")

    if not auth.canAccessTask(reqUser, task):
        raise HTTPException(status_code=404, detail="Not Found!")

    return task


@router.patch("/{taskID}")
def updateTask(
    taskID: int,
    updateData: TaskUpdate,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> TaskRead:
    task = taskUtils.getTask(taskID, db)
    if not task:
        raise HTTPException(status_code=404, detail="Not Found!")

    if not auth.canAccessTask(reqUser, task):
        raise HTTPException(status_code=404, detail="Not Found!")

    return taskUtils.updateTask(task, updateData, db)


@router.delete("/{taskID}")
def deleteTask(
    taskID: int,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> dict[str, str]:
    task = taskUtils.getTask(taskID, db)
    if not task:
        raise HTTPException(status_code=404, detail="Not Found!")

    if not auth.canAccessTask(reqUser, task):
        raise HTTPException(status_code=404, detail="Not Found!")

    taskUtils.deleteTask(task, db)
    return {"message": "Task Deleted"}


def notifyDeadline():
    pass
