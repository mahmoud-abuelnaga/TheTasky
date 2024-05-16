from .base import session, BASE_URL

def get_user_tasks(token):
    response = session.get(f"{BASE_URL}/users/me", headers={"token-bearer": token})
    tasks = []
    if response.ok:
        tasks = response.json()["assignedTasks"]
    return tasks

def create_task(token, task):
    response = session.post(
        f"{BASE_URL}/tasks/create",
        headers={"token-bearer": token},
        json=task
    )
    return response.ok

def delete_task(token, task_id):
    response = session.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers={"token-bearer": token},
    )
    return response.ok


def update_task(token, task_id, field_name, field):
    response = session.patch(
        f"{BASE_URL}/tasks/{task_id}",
        headers={"token-bearer": token},
        json={field_name: field}
    )
    return response.ok
