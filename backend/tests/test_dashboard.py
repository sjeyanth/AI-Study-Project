import uuid

from tests.conftest import auth_user, client

def test_dashboard_requires_auth():

    response = client.get(
        "/dashboard"
    )

    assert response.status_code == 401

def test_dashboard_empty(
    auth_user
):

    response = client.get(
        "/dashboard",
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_tasks"] == 0
    assert data["completed_tasks"] == 0
    assert data["pending_tasks"] == 0

    assert data["total_goals"] == 0
    assert data["completed_goals"] == 0

    assert data["average_goal_progress"] == 0

def test_dashboard_with_data(
        auth_user        
):
    client.post(
        "/tasks",
        json={
            "title": "Task 1",
            "description": "Completed",
            "completed": True
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/tasks",
        json={
            "title": "Task 2",
            "description": "Completed",
            "completed": True
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/tasks",
        json={
            "title": "Task 3",
            "description": "Pending",
            "completed": False
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/goals",
        json={
            "title": "Goal 1",
            "description": "Completed Goal",
            "target_date": "2030-01-01T00:00:00Z",
            "status": "completed",
            "progress": 100
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/goals",
        json={
            "title": "Goal 2",
            "description": "In Progress Goal",
            "target_date": "2030-01-01T00:00:00Z",
            "status": "in_progress",
            "progress": 50
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )
    
    response = client.get(
        "/dashboard",
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_tasks"] == 3

    assert data["completed_tasks"] == 2

    assert data["pending_tasks"] == 1

    assert data["total_goals"] == 2

    assert data["completed_goals"] == 1

    assert data["average_goal_progress"] == 75
