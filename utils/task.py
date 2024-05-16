# external modules
from sqlalchemy.orm import Session

# our modules
from models.task import TaskModel
from schemas.task import TaskCreate, TaskUpdate


def createTask(task: TaskCreate, creatorID: int, db: Session) -> TaskModel:
    task = TaskModel(**task.model_dump(), creatorID=creatorID)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def getTask(taskID: int, db: Session) -> TaskModel:
    return db.query(TaskModel).filter(TaskModel.id == taskID).first()


def updateTask(
    task: TaskModel | int, updateData: TaskUpdate, db: Session
) -> TaskModel | None:
    if type(task) is int:
        task = db.query(TaskModel).filter(TaskModel.id == task).first()
        if not task:
            raise None

    for key, value in updateData.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def deleteTask(task: int | TaskModel, db: Session) -> TaskModel | None:
    if type(task) is int:
        task = db.query(TaskModel).filter(TaskModel.id == task).first()
        if not task:
            raise None

    db.delete(task)
    db.commit()
    return task
