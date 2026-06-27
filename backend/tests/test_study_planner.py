from app.ai.schemas.ai import StudyPlannerResponse
from tests.conftest import client


def _payload():
    return {
        "title": "Final Exam Plan",
        "subjects": [
            {
                "name": "Database Systems",
                "exam_date": "2030-07-10",
                "difficulty": "Hard"
            },
            {
                "name": "AI",
                "exam_date": "2030-07-15",
                "difficulty": "Medium"
            }
        ],
        "assignment_deadlines": [],
        "available_hours_per_day": 2,
        "preferred_session_length": 60,
        "notes": "Focus on weak topics"
    }


def _mock_plan():
    return StudyPlannerResponse(
        weekly_schedule=[
            {
                "day": "Monday",
                "total_minutes": 120,
                "sessions": [
                    {
                        "subject": "Database Systems",
                        "duration_minutes": 60,
                        "activity": "Study indexing",
                        "type": "study"
                    },
                    {
                        "subject": "Break",
                        "duration_minutes": 10,
                        "activity": "Reset",
                        "type": "break"
                    }
                ]
            }
        ],
        daily_plan=[
            {
                "date": "2030-07-01",
                "focus": "Database Systems",
                "sessions": [
                    {
                        "subject": "Database Systems",
                        "duration_minutes": 60,
                        "activity": "Practice ER diagrams",
                        "type": "study"
                    }
                ]
            }
        ],
        priority_order=[
            {
                "subject": "Database Systems",
                "reason": "Earlier and harder exam",
                "rank": 1
            }
        ],
        recommended_study_duration=[
            {
                "subject": "Database Systems",
                "minutes_per_week": 360,
                "reason": "Hard subject"
            }
        ],
        revision_schedule=[
            {
                "subject": "Database Systems",
                "date": "2030-07-08",
                "focus": "Review weak areas"
            }
        ],
        break_suggestions=[
            "Take short breaks between sessions"
        ],
        study_tips=[
            "Use active recall"
        ],
        explanation="Database Systems is scheduled first because the exam is earlier."
    )


def test_study_planner_requires_auth():
    response = client.post(
        "/study-planner",
        json=_payload()
    )

    assert response.status_code == 401


def test_create_study_plan_saves_generated_plan(
    auth_user,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.study_plan_service.study_planner",
        lambda request: _mock_plan()
    )

    response = client.post(
        "/study-planner",
        json=_payload(),
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Final Exam Plan"
    assert data["subject_count"] == 2
    assert data["ai_reasoning"] == _mock_plan().explanation
    assert data["weekly_plan_json"]["weekly_schedule"][0]["day"] == "Monday"


def test_get_study_plans_returns_current_user_plans(
    auth_user,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.study_plan_service.study_planner",
        lambda request: _mock_plan()
    )

    client.post(
        "/study-planner",
        json=_payload(),
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    response = client.get(
        "/study-planner",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert "weekly_plan_json" not in data[0]
    assert "subject_count" in data[0]


def test_study_plan_cannot_be_read_by_another_user(
    user_factory,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.study_plan_service.study_planner",
        lambda request: _mock_plan()
    )

    first_user = user_factory()
    second_user = user_factory()

    create_response = client.post(
        "/study-planner",
        json=_payload(),
        headers={
            "Authorization": f"Bearer {first_user['token']}"
        }
    )
    study_plan_id = create_response.json()["id"]

    response = client.get(
        f"/study-planner/{study_plan_id}",
        headers={
            "Authorization": f"Bearer {second_user['token']}"
        }
    )

    assert response.status_code == 404


def test_delete_study_plan(
    auth_user,
    monkeypatch
):
    monkeypatch.setattr(
        "app.services.study_plan_service.study_planner",
        lambda request: _mock_plan()
    )

    create_response = client.post(
        "/study-planner",
        json=_payload(),
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )
    study_plan_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/study-planner/{study_plan_id}",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert delete_response.status_code == 200

    get_response = client.get(
        f"/study-planner/{study_plan_id}",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert get_response.status_code == 404
