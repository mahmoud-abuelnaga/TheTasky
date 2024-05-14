# external modules
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# our modules
from utils import database, team as teamUtils, user as userUtils, auth
from schemas.team import TeamCreate, TeamRead, AddMember, UpdateTeam, RemoveMember
from models.user import UserModel

# setup
router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.post("/create")
def createTeam(
    team: TeamCreate,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> TeamRead:
    try:
        team = teamUtils.createTeam(team, reqUser.id, db)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return team


@router.get("/{teamID}")
def getTeam(
    teamID: int,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> TeamRead:
    team = teamUtils.getTeam(teamID, db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if not auth.isMemberInTeam(reqUser, team) and team.creatorID != reqUser.id:
        raise HTTPException(status_code=404, detail="Team not found")

    return team


@router.patch("/{teamID}")
def updateTeam(
    teamID: int,
    data: UpdateTeam,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> TeamRead:
    team = teamUtils.getTeam(teamID, db)
    if not team or team.creatorID != reqUser.id:
        raise HTTPException(status_code=404, detail="Team not found")

    team.name = data.name
    db.commit()
    db.refresh(team)

    return team


@router.delete("/{teamID}")
def deleteTeam(
    teamID: int,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> dict[str, str]:
    team = teamUtils.getTeam(teamID, db)
    if not team or team.creatorID != reqUser.id:
        raise HTTPException(status_code=404, detail="Team not found")

    db.delete(team)
    db.commit()

    return {"message": "Team Deleted"}


@router.patch("/{teamID}/add-member")
def addMember(
    teamID: int,
    data: AddMember,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> dict[str, str]:
    team = teamUtils.getTeam(teamID, db)
    if not team or team.creatorID != reqUser.id:
        raise HTTPException(status_code=404, detail="Team not found")

    member = userUtils.getUser(data.email, db)
    if not member:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    member = teamUtils.addMember(team, member, db)
    if not member:
        raise HTTPException(
            status_code=400, detail="User doesn't exist or already in the team"
        )

    return {"message": "Success"}


@router.patch("/{teamID}/remove-member")
def removeMember(
    teamID: int,
    data: RemoveMember,
    db: Session = Depends(database.getSession),
    reqUser: UserModel = Depends(auth.getRequestUser),
) -> dict[str, str]:
    team = teamUtils.getTeam(teamID, db)
    if not team or team.creatorID != reqUser.id:
        raise HTTPException(status_code=404, detail="Team not found")

    member = userUtils.getUser(data.memberID, db)
    if not member:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    inTeam = teamUtils.removeMember(team, member, db)
    if not inTeam:
        raise HTTPException(status_code=400, detail="User isn't in the Team")

    return {"message": "Success"}
