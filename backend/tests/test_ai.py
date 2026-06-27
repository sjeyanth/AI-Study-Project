from tests.conftest import client


# ==========================
# Authentication Tests
# ==========================

def test_summarize_note_requires_auth():

    response = client.post(
        "/ai/summarize-note",
        json={
            "content": "Test Note"
        }
    )

    assert response.status_code == 401


def test_generate_email_requires_auth():

    response = client.post(
        "/ai/generate-mail",
        json={
            "purpose": "Request Extension"
        }
    )

    assert response.status_code == 401


def test_task_breakdown_requires_auth():

    response = client.post(
        "/ai/task-breakdown",
        json={
            "goal": "Learn React"
        }
    )

    assert response.status_code == 401


def test_budget_insights_requires_auth():

    response = client.post(
        "/ai/budget-insights",
        json={
            "budget_summary": "Budget 10000, Spent 7000"
        }
    )

    assert response.status_code == 401


def test_study_planner_requires_auth():

    response = client.post(
        "/ai/study-planner",
        json={
            "subjects": [
                {
                    "name": "Database Systems",
                    "exam_date": "2026-07-10",
                    "difficulty": "Hard"
                }
            ],
            "available_hours_per_day": 2,
            "preferred_session_length": 60
        }
    )

    assert response.status_code == 401


# ==========================
# Summarize Note
# ==========================

def test_summarize_note(
    auth_user
):

    response = client.post(
        "/ai/summarize-note",
        json={
            "content":
            "FastAPI is a modern Python web framework."
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data

    assert isinstance(
        data["summary"],
        str
    )


# ==========================
# Generate Email
# ==========================

def test_generate_email(
    auth_user
):

    response = client.post(
        "/ai/generate-mail",
        json={
            "purpose":
            "Request project deadline extension"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "email" in data

    assert isinstance(
        data["email"],
        str
    )


# ==========================
# Task Breakdown
# ==========================

def test_task_breakdown(
    auth_user
):

    response = client.post(
        "/ai/task-breakdown",
        json={
            "goal":
            "Learn React"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "tasks" in data

    assert isinstance(
        data["tasks"],
        list
    )

    assert len(
        data["tasks"]
    ) > 0


# ==========================
# Budget Insights
# ==========================

def test_budget_insights(
    auth_user
):

    response = client.post(
        "/ai/budget-insights",
        json={
            "budget_summary":
            "Budget 10000, Spent 7000"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "insights" in data

    assert isinstance(
        data["insights"],
        str
    )
