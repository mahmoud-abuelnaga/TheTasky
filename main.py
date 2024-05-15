# external modules
from datetime import datetime
from fastapi import FastAPI, Request, status, HTTPException, Depends
from sqlalchemy.orm import Session

# Models
from models.user import UserModel
from models.task import TaskModel
from models.reminder import ReminderModel
from models.team import TeamModel

# our modules
from utils import database, auth, user as userUtils, bacground_tasks

# routers
from routers import user, task, team, auth, reminder

# Helpers
Base = database.getBase()
engine = database.getEngine()

# setup
Base.metadata.create_all(bind=engine)
app = FastAPI()

# routes
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(team.router)
app.include_router(reminder.router)


# start background tasks

bacground_tasks.start_scheduler()


# routes
@app.get("/")
def root():
    print(datetime.now())
    return {"message": "Hello World!"}


# @app.middleware("http")
# async def getRequestUser(request: Request, call_next):
#     token = request.headers.get("Authorization")
#     if token:
#         email = await auth.decodeToken(token)
#         if email:
#             request.state.user = userUtils.getUser(email, next(database.getSession()))

#     response = await call_next(request)
#     return response
