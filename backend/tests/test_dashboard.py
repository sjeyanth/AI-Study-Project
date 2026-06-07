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

    assert data["total_notes"] == 0

    assert data["total_reminders"] == 0

    assert data["total_budget"] == 0

    assert data["total_spent"] == 0

    assert data["remaining_budget"] == 0
    

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

    client.post(
        "/notes",
        json={
            "title": "Note 1",
            "content": "Note content 1",
            "tags": "study"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/notes",
        json={
            "title": "Note 2",
            "content": "Note content 2",
            "tags": "review"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/reminders",
        json={
            "title": "Reminder 1",
            "description": "Reminder description 1",
            "tags": "study",
            "due_date": "2030-01-01T09:00:00Z",
            "completed": False
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/reminders",
        json={
            "title": "Reminder 2",
            "description": "Reminder description 2",
            "tags": "follow-up",
            "due_date": "2030-01-02T09:00:00Z",
            "completed": False
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/budgets",
        json={
            "month": 6,
            "year": 2026,
            "total_budget": 10000,
            "currency": "INR"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/expenses",
        json={
            "title": "Expense 1",
            "amount": 1000,
            "expense_date": "2030-01-01T12:00:00Z",
            "category": "General",
            "notes": "Expense note 1"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/expenses",
        json={
            "title": "Expense 2",
            "amount": 500,
            "expense_date": "2030-01-02T12:00:00Z",
            "category": "General",
            "notes": "Expense note 2"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    client.post(
        "/expenses",
        json={
            "title": "Expense 3",
            "amount": 500,
            "expense_date": "2030-01-03T12:00:00Z",
            "category": "General",
            "notes": "Expense note 3"
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

    assert data["total_notes"] == 2

    assert data["total_reminders"] == 2

    assert data["total_budget"] == 10000

    assert data["total_spent"] == 2000

    assert data["remaining_budget"] == 8000
