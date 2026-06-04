import uuid
from datetime import datetime, timezone

from tests.conftest import client


def test_create_expense(auth_user):

    response = client.post(
        "/expenses",
        json={
            "title": "New Expense",
            "amount": 499.99,
            "expense_date": "2026-06-05T12:00:00Z",
            "category": "Shopping",
            "notes": "Created in test"
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Expense"
    assert data["amount"] == 499.99
    expected_dt = datetime(2026, 6, 5, 12, 0, 0, tzinfo=timezone.utc)
    actual_dt = datetime.fromisoformat(data["expense_date"])
    assert actual_dt.astimezone(timezone.utc) == expected_dt
    assert data["category"] == "Shopping"
    assert data["notes"] == "Created in test"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_expenses_with_filters_and_search(auth_user):

    unique_title = f"Expense_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/expenses",
        json={
            "title": unique_title,
            "amount": 150.0,
            "expense_date": "2026-06-04T08:00:00Z",
            "category": "Food",
            "notes": "Searchable note"
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    response = client.get(
        f"/expenses?search={unique_title}&category=Food&start_date=2026-06-01T00:00:00Z&end_date=2026-06-30T23:59:59Z",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    expenses = response.json()

    titles = [expense["title"] for expense in expenses]

    assert unique_title in titles


def test_get_expense_by_id(test_expense):

    expense = test_expense["expense"]
    user = test_expense["user"]

    response = client.get(
        f"/expenses/{expense['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == expense["id"]
    assert data["title"] == expense["title"]


def test_update_expense(test_expense):

    expense = test_expense["expense"]
    user = test_expense["user"]

    updated_payload = {
        "title": "Updated Expense",
        "amount": 300.0,
        "expense_date": "2026-06-06T09:30:00Z",
        "category": "Transport",
        "notes": "Updated notes"
    }

    response = client.put(
        f"/expenses/{expense['id']}",
        json=updated_payload,
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == updated_payload["title"]
    assert data["amount"] == updated_payload["amount"]
    assert data["category"] == updated_payload["category"]


def test_delete_expense(test_expense):

    expense = test_expense["expense"]
    user = test_expense["user"]

    delete_response = client.delete(
        f"/expenses/{expense['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Expense deleted successfully"
    }

    fetch_response = client.get(
        f"/expenses/{expense['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert fetch_response.status_code == 404

    assert fetch_response.json() == {
        "detail": "Expense not found"
    }


def test_user_cannot_access_other_users_expense(user_factory):

    user_a = user_factory()
    user_b = user_factory()

    expense_response = client.post(
        "/expenses",
        json={
            "title": "Private Expense",
            "amount": 50.0,
            "expense_date": "2026-06-03T08:00:00Z",
            "category": "Misc",
            "notes": None
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    expense_id = expense_response.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Expense not found"
    }
