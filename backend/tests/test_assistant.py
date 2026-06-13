from tests.conftest import client


# ==========================
# Authentication
# ==========================

def test_assistant_chat_requires_auth():

    response = client.post(
        "/assistant/chat",
        json={
            "message":
            "Summarize my notes"
        }
    )

    assert response.status_code == 401


# ==========================
# Summarizer Intent
# ==========================

def test_assistant_summarize_intent(
    auth_user
):

    response = client.post(
        "/assistant/chat",
        json={
            "message":
            "Summarize my notes"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data

    assert "summarize" in (
        data["response"]
        .lower()
    )


# ==========================
# Email Intent
# ==========================

def test_assistant_email_intent(
    auth_user
):

    response = client.post(
        "/assistant/chat",
        json={
            "message":
            "Help me write an email"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data

    assert "email" in (
        data["response"]
        .lower()
    )


# ==========================
# Task Intent
# ==========================

def test_assistant_task_intent(
    auth_user
):

    response = client.post(
        "/assistant/chat",
        json={
            "message":
            "Help me plan my goal"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data

    assert "task" in (
        data["response"]
        .lower()
    )


# ==========================
# Budget Intent
# ==========================

def test_assistant_budget_intent(
    auth_user
):

    response = client.post(
        "/assistant/chat",
        json={
            "message":
            "Analyze my spending"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data

    assert (
        "budget" in
        data["response"].lower()
        or
        "spending" in
        data["response"].lower()
    )


# ==========================
# Fallback Intent
# ==========================

def test_assistant_unknown_intent(
    auth_user
):

    response = client.post(
        "/assistant/chat",
        json={
            "message":
            "Hello assistant"
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data

    assert isinstance(
        data["response"],
        str
    )