import uuid

from tests.conftest import client


def test_create_reminder(auth_user):

    response = client.post(
        "/reminders",
        json={
            "title": "New Reminder",
            "description": "Created in test",
            "tags": "#reminder",
            "due_date": "2026-06-05T10:00:00Z",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Reminder"
    assert data["description"] == "Created in test"
    assert data["tags"] == "#reminder"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_reminders_with_pagination(auth_user):

    title_a = f"Reminder_{uuid.uuid4().hex[:8]}"
    title_b = f"Reminder_{uuid.uuid4().hex[:8]}"

    for title in [title_a, title_b]:
        response = client.post(
            "/reminders",
            json={
                "title": title,
                "description": "Pagination check",
                "tags": None,
                "due_date": None,
                "completed": False
            },
            headers={
                "Authorization": f"Bearer {auth_user['token']}"
            }
        )
        assert response.status_code == 200

    first_page = client.get(
        "/reminders?skip=0&limit=1&sort_by=title&sort_dir=asc",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert first_page.status_code == 200

    assert len(first_page.json()) == 1

    second_page = client.get(
        "/reminders?skip=1&limit=1&sort_by=title&sort_dir=asc",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert second_page.status_code == 200

    assert len(second_page.json()) == 1


def test_search_reminders(auth_user):

    unique_title = f"Search_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/reminders",
        json={
            "title": unique_title,
            "description": "Searchable description",
            "tags": None,
            "due_date": None,
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    search_response = client.get(
        f"/reminders?search={unique_title}",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert search_response.status_code == 200

    titles = [reminder["title"] for reminder in search_response.json()]

    assert unique_title in titles


def test_get_reminder_by_id(test_reminder):

    reminder = test_reminder["reminder"]
    user = test_reminder["user"]

    response = client.get(
        f"/reminders/{reminder['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reminder["id"]
    assert data["title"] == reminder["title"]


def test_update_reminder(test_reminder):

    reminder = test_reminder["reminder"]
    user = test_reminder["user"]

    updated_payload = {
        "title": "Updated Reminder",
        "description": "Updated description",
        "tags": "#updated",
        "due_date": None,
        "completed": True
    }

    response = client.put(
        f"/reminders/{reminder['id']}",
        json=updated_payload,
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == updated_payload["title"]
    assert data["description"] == updated_payload["description"]
    assert data["tags"] == updated_payload["tags"]
    assert data["completed"] is True


def test_delete_reminder(test_reminder):

    reminder = test_reminder["reminder"]
    user = test_reminder["user"]

    delete_response = client.delete(
        f"/reminders/{reminder['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Reminder deleted successfully"
    }

    fetch_response = client.get(
        f"/reminders/{reminder['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert fetch_response.status_code == 404

    assert fetch_response.json() == {
        "detail": "Reminder not found"
    }


def test_user_cannot_access_other_users_reminder(user_factory):

    user_a = user_factory()
    user_b = user_factory()

    reminder_response = client.post(
        "/reminders",
        json={
            "title": "Private Reminder",
            "description": "Only User A should see this",
            "tags": None,
            "due_date": None,
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    reminder_id = reminder_response.json()["id"]

    response = client.get(
        f"/reminders/{reminder_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Reminder not found"
    }
