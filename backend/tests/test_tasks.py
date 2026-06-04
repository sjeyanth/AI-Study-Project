import uuid

from tests.conftest import client


def test_create_task(auth_user):

    response = client.post(
        "/tasks",
        json={
            "title": "New Task",
            "description": "Created in test",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Task"

    assert data["description"] == "Created in test"

    assert data["completed"] is False

    assert "id" in data


def test_get_tasks(auth_user):

    task_title = f"Task_{uuid.uuid4().hex[:8]}"

    create_response = client.post(
        "/tasks",
        json={
            "title": task_title,
            "description": "List check",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert create_response.status_code == 200

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    tasks = response.json()

    titles = [task["title"] for task in tasks]

    assert task_title in titles


def test_get_task_by_id(test_task):

    task = test_task["task"]

    user = test_task["user"]

    response = client.get(
        f"/tasks/{task['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task["id"]

    assert data["title"] == task["title"]


def test_update_task(test_task):

    task = test_task["task"]

    user = test_task["user"]

    updated_payload = {
        "title": "Updated Task",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(
        f"/tasks/{task['id']}",
        json=updated_payload,
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == updated_payload["title"]

    assert data["description"] == updated_payload["description"]

    assert data["completed"] is True


def test_delete_task(test_task):

    task = test_task["task"]

    user = test_task["user"]

    delete_response = client.delete(
        f"/tasks/{task['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Task deleted successfully"
    }

    fetch_response = client.get(
        f"/tasks/{task['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert fetch_response.status_code == 404

    assert fetch_response.json() == {
        "detail": "Task not found"
    }


def test_user_can_only_see_own_tasks(user_factory):

    user_a = user_factory()

    user_b = user_factory()

    task_title = f"UserATask_{uuid.uuid4().hex[:8]}"

    create_response = client.post(
        "/tasks",
        json={
            "title": task_title,
            "description": "User A Task",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    assert create_response.status_code == 200

    tasks_response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert tasks_response.status_code == 200

    tasks = tasks_response.json()

    titles = [task["title"] for task in tasks]

    assert task_title not in titles


def test_user_cannot_access_other_users_task(user_factory):

    user_a = user_factory()

    user_b = user_factory()

    task_response = client.post(
        "/tasks",
        json={
            "title": "Secret Task",
            "description": "Only User A should see this",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    task_id = task_response.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found"
    }


def test_user_cannot_update_other_users_task(user_factory):

    user_a = user_factory()

    user_b = user_factory()

    task_response = client.post(
        "/tasks",
        json={
            "title": "Locked Task",
            "description": "Only User A should edit",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    task_id = task_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Hacked Title",
            "description": "Hacked",
            "completed": True
        },
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found"
    }


def test_user_cannot_delete_other_users_task(user_factory):

    user_a = user_factory()

    user_b = user_factory()

    task_response = client.post(
        "/tasks",
        json={
            "title": "Protected Task",
            "description": "Only User A should delete",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    task_id = task_response.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found"
    }
