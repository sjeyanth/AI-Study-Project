import uuid

from tests.conftest import client


def test_create_budget(auth_user):

    response = client.post(
        "/budgets",
        json={
            "month": 6,
            "year": 2026,
            "total_budget": 35000.0,
            "currency": "INR"
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["month"] == 6
    assert data["year"] == 2026
    assert data["total_budget"] == 35000.0
    assert data["currency"] == "INR"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_budgets_with_filters(auth_user):

    response = client.post(
        "/budgets",
        json={
            "month": 5,
            "year": 2026,
            "total_budget": 20000.0,
            "currency": "INR"
        },
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    response = client.get(
        "/budgets?month=5&year=2026",
        headers={
            "Authorization": f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    budgets = response.json()

    assert len(budgets) >= 1

    for budget in budgets:
        assert budget["month"] == 5
        assert budget["year"] == 2026


def test_get_budget_by_id(test_budget):

    budget = test_budget["budget"]
    user = test_budget["user"]

    response = client.get(
        f"/budgets/{budget['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == budget["id"]
    assert data["month"] == budget["month"]


def test_update_budget(test_budget):

    budget = test_budget["budget"]
    user = test_budget["user"]

    updated_payload = {
        "month": 7,
        "year": 2026,
        "total_budget": 45000.0,
        "currency": "INR"
    }

    response = client.put(
        f"/budgets/{budget['id']}",
        json=updated_payload,
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["month"] == updated_payload["month"]
    assert data["year"] == updated_payload["year"]
    assert data["total_budget"] == updated_payload["total_budget"]


def test_delete_budget(test_budget):

    budget = test_budget["budget"]
    user = test_budget["user"]

    delete_response = client.delete(
        f"/budgets/{budget['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Budget deleted successfully"
    }

    fetch_response = client.get(
        f"/budgets/{budget['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert fetch_response.status_code == 404

    assert fetch_response.json() == {
        "detail": "Budget not found"
    }


def test_user_cannot_access_other_users_budget(user_factory):

    user_a = user_factory()
    user_b = user_factory()

    budget_response = client.post(
        "/budgets",
        json={
            "month": 8,
            "year": 2026,
            "total_budget": 15000.0,
            "currency": "INR"
        },
        headers={
            "Authorization": f"Bearer {user_a['token']}"
        }
    )

    budget_id = budget_response.json()["id"]

    response = client.get(
        f"/budgets/{budget_id}",
        headers={
            "Authorization": f"Bearer {user_b['token']}"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Budget not found"
    }
