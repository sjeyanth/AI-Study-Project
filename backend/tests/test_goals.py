import uuid

from tests.conftest import client


def test_create_goal(auth_user):

    response = client.post(
        "/goals",
        json={
            "title": "New Goal",
            "description": "Created in test",
            "target_date": "2026-07-15T00:00:00Z",
            "status": "in_progress",
            "progress": 20
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Goal"
    assert data["description"] == "Created in test"
    assert data["status"] == "in_progress"
    assert data["progress"] == 20
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_goals(auth_user):

    goal_title = f"Goal_{uuid.uuid4().hex[:8]}"

    create_response = client.post(
        "/goals",
        json={
            "title": goal_title,
            "description": "List check",
            "target_date": "2026-08-01T00:00:00Z",
            "status": "planned",
            "progress": 10
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert create_response.status_code == 200

    response = client.get(
        "/goals",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    goals = response.json()

    titles = [goal["title"] for goal in goals]

    assert goal_title in titles


def test_get_goal_by_id(test_goal):

    goal = test_goal["goal"]
    user = test_goal["user"]

    response = client.get(
        f"/goals/{goal['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == goal["id"]
    assert data["title"] == goal["title"]


def test_update_goal(test_goal):

    goal = test_goal["goal"]
    user = test_goal["user"]

    updated_payload = {
        "title": "Updated Goal",
        "description": "Updated description",
        "target_date": "2026-08-15T00:00:00Z",
        "status": "completed",
        "progress": 100
    }

    response = client.put(
        f"/goals/{goal['id']}",
        json=updated_payload,
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == updated_payload["title"]
    assert data["description"] == updated_payload["description"]
    assert data["status"] == updated_payload["status"]
    assert data["progress"] == updated_payload["progress"]


def test_delete_goal(test_goal):

    goal = test_goal["goal"]
    user = test_goal["user"]

    delete_response = client.delete(
        f"/goals/{goal['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Goal deleted successfully"
    }

    fetch_response = client.get(
        f"/goals/{goal['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert fetch_response.status_code == 404

    assert fetch_response.json() == {
        "detail": "Goal not found"
    }


def test_user_cannot_access_other_users_goal(user_factory):

    user_a = user_factory()
    user_b = user_factory()

    goal_response = client.post(
        "/goals",
        json={
            "title": "Private Goal",
            "description": "Only User A should see this",
            "target_date": "2026-09-01T00:00:00Z",
            "status": "planned",
            "progress": 5
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    goal_id = goal_response.json()["id"]

    response = client.get(
        f"/goals/{goal_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Goal not found"
    }