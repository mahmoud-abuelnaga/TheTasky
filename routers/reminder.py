from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session


from utils import database, auth, remainder as remainderUtils
from models.user import UserModel
from schemas import remainder
from models.reminder import ReminderModel
from datetime import datetime

router = APIRouter(
    prefix="/remainder",
    tags=["remainders"],
)


@router.post("/add", response_model=remainder.Reminder)
def createReminder(
    task: remainder.ReminderCreate,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
):
    try:
        task = remainderUtils.createRemainder(task, reqUser.id, db)
        print(datetime.now())
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{id}", response_model=remainder.Reminder)
def updateReminder(
    task: remainder.ReminderCreate,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
):
    task_q = db.query(ReminderModel).filter(ReminderModel.id == id)
    task_r = task_q.first()
    if not task_r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="404 not found"
        )
    task_q.update(task.model_dump(), synchronize_session=False)
    db.commit()
    return task_q.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTask(
    id: int,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
):

    task_q = db.query(ReminderModel).filter(ReminderModel.id == id)
    task = task_q.first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="404 not found"
        )

    task_q.delete(False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
