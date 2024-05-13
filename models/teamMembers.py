# external modules
from sqlalchemy import Table, Column, ForeignKey

# our modules
from utils import database

# helpers
Base = database.getBase()

# definitions
associationTable = Table(
    "team_members",
    Base.metadata,
    Column(
        "teamID",
        ForeignKey("teams.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
    Column(
        "userID",
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
)
