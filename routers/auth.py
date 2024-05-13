# external modules
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# our modules
from schemas.user import UserSignup, UserRead, UserLogin
from utils import database
from utils import user as userUtils, hashing, auth

# setup
router = APIRouter(
    tags=["users"],
)


@router.post("/signup", response_model=UserRead)
def createUser(userData: UserSignup, db: Session = Depends(database.getSession)):
    try:
        user = userUtils.createUser(userData, db)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return user


@router.post("/login")
def login(loginData: UserLogin, db: Session = Depends(database.getSession)):
    user = userUtils.getUser(loginData.email, db)
    if not user or not hashing.verify(loginData.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"token": auth.createAccessToken({"id": user.id, "email": user.email})}
