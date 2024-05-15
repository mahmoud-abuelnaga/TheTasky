from .base import session, BASE_URL

def get_user_tasks(token):
    response = session.get(
        f"{BASE_URL}/users/me/tasks", headers={"token-bearer": token}
    )
    if response.ok:
        info = response.json()
        return info

def create_task(token, task):
    response = session.post(
        f"{BASE_URL}/tasks/create",
        headers={"token-bearer": token},
        json=task
    )
    return response.ok