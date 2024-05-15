from .base import session, BASE_URL


def create_user(name: str, email: str, password: str):
    body = {"name": name, "email": email, "password": password}
    response = session.post(f"{BASE_URL}/signup", json=body)
    return response.ok


def get_user_token(email, password):
    body = {"email": email, "password": password}
    response = session.post(f"{BASE_URL}/login", json=body)
    token = None
    if response.ok:
        token = response.json()["token"]
    return response.ok, token


def get_user_details(token):
    response = session.get(f"{BASE_URL}/users/me", headers={"token-bearer": token})
    name, email = "", ""
    if response.ok:
        info = response.json()
        name, email = info["name"], info["email"]
    return name, email


def get_user_teams(token):
    response = session.get(f"{BASE_URL}/users/me/teams", headers={"token-bearer": token})
    name, email = None, None
    teams = None
    if response.ok:
        teams = response.json()
    return teams
