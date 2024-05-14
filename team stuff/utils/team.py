# external modules
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

# our modules
from models.team import TeamModel
from models.user import UserModel
from models.teamMembers import associationTable
from schemas.team import TeamCreate


def createTeam(teamData: TeamCreate, creatorID: int, db: Session) -> TeamModel:
    team = TeamModel(**teamData.model_dump(), creatorID=creatorID)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def getTeam(teamID: int, db: Session) -> TeamModel:
    return db.query(TeamModel).filter(TeamModel.id == teamID).first()


def addMember(team: TeamModel, member: UserModel, db: Session) -> UserModel | None:
    if not team:
        return None
    try:
        team.members.append(member)
    except Exception as e:
        return None

    db.commit()
    db.refresh(member)
    return member


def removeMember(team: TeamModel, member: UserModel, db: Session) -> bool:
    if not team or not member:
        return False

    try:
        team.members.remove(member)
    except Exception as e:
        return False

    db.commit()
    db.refresh(member)
    return True
