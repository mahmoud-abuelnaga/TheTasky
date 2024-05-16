from .base import session, BASE_URL
from .user import get_user_details

def create_team(token, team_name):
    response = session.post(
        f"{BASE_URL}/teams/create",
        headers={"token-bearer": token},
        json={"name": team_name},
    )
    team_id = None
    if response.ok:
        team_id = response.json()["id"]
    return response.ok, team_id


def add_member(token, team_id, email):
    response = session.patch(
        f"{BASE_URL}/teams/{team_id}/add-member",
        headers={"token-bearer": token},
        json={"email": email},
    )
    return response.ok

def join_team(token, team_id):
    my_email, _ = get_user_details(token)
    add_member(token, team_id, my_email)

def get_team_members(token, team_id):

    response = session.get(
        f"{BASE_URL}/teams/{team_id}/members",
        headers={"token-bearer": token},
    )
    members = []
    if response.ok:
        members = response.json()
    return members


def get_team_name(token, team_id):
    response = session.get(
        f"{BASE_URL}/teams/{team_id}",
        headers={"token-bearer": token},
    )
    name = ""
    if response.ok:
        name = response.json()["name"]
    return name