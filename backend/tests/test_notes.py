import uuid

from tests.conftest import client


def test_create_note(auth_user):

    response = client.post(
        "/notes",
        json={
            "title": "New Note",
            "content": "Created in test",
            "tags": "#fastapi"
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Note"
    assert data["content"] == "Created in test"
    assert data["tags"] == "#fastapi"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_notes_with_pagination(auth_user):

    title_a = f"Note_{uuid.uuid4().hex[:8]}"
    title_b = f"Note_{uuid.uuid4().hex[:8]}"

    for title in [title_a, title_b]:
        response = client.post(
            "/notes",
            json={
                "title": title,
                "content": "Pagination check",
                "tags": None
            },
            headers={
                "Authorization": f"Bearer {auth_user['token']}"
            }
        )
        assert response.status_code == 200

    first_page = client.get(
        "/notes?skip=0&limit=1&sort_by=title&sort_dir=asc",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert first_page.status_code == 200

    assert len(first_page.json()) == 1

    second_page = client.get(
        "/notes?skip=1&limit=1&sort_by=title&sort_dir=asc",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert second_page.status_code == 200

    assert len(second_page.json()) == 1


def test_search_notes(auth_user):

    unique_title = f"Search_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/notes",
        json={
            "title": unique_title,
            "content": "Searchable content",
            "tags": "#search"
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    search_response = client.get(
        f"/notes?search={unique_title}",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert search_response.status_code == 200

    titles = [note["title"] for note in search_response.json()]

    assert unique_title in titles


def test_get_note_by_id(test_note):

    note = test_note["note"]
    user = test_note["user"]

    response = client.get(
        f"/notes/{note['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == note["id"]
    assert data["title"] == note["title"]


def test_update_note(test_note):

    note = test_note["note"]
    user = test_note["user"]

    updated_payload = {
        "title": "Updated Note",
        "content": "Updated content",
        "tags": "#updated"
    }

    response = client.put(
        f"/notes/{note['id']}",
        json=updated_payload,
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == updated_payload["title"]
    assert data["content"] == updated_payload["content"]
    assert data["tags"] == updated_payload["tags"]


def test_delete_note(test_note):

    note = test_note["note"]
    user = test_note["user"]

    delete_response = client.delete(
        f"/notes/{note['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Note deleted successfully"
    }

    fetch_response = client.get(
        f"/notes/{note['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert fetch_response.status_code == 404

    assert fetch_response.json() == {
        "detail": "Note not found"
    }


def test_user_cannot_access_other_users_note(user_factory):

    user_a = user_factory()
    user_b = user_factory()

    note_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Only User A should see this",
            "tags": None
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    note_id = note_response.json()["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Note not found"
    }
