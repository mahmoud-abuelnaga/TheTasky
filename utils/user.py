# external modules
from sqlalchemy.orm import Session

# our modules
from models.user import UserModel
from schemas.user import UserSignup, UserUpdate


# Definition
def createUser(userData: UserSignup, db: Session) -> UserModel:
    user = UserModel(**userData.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def getUser(userID: int | str, db: Session) -> UserModel:
    if type(userID) is int:
        return db.query(UserModel).filter(UserModel.id == userID).first()
    else:
        return db.query(UserModel).filter(UserModel.email == userID).first()


def deleteUser(user: int | UserModel, db: Session) -> UserModel:
    if type(user) is int:
        user = db.query(UserModel).filter(UserModel.id == user).first()
        if not user:
            return None

    db.delete(user)
    db.commit()
    return user


def updateUser(user: int | UserModel, data: UserUpdate, db: Session) -> UserModel:
    if type(user) is int:
        user = db.query(UserModel).filter(UserModel.id == user).first()
        if not user:
            return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
