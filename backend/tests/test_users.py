import uuid

from tests.conftest import client


def test_register_user():

    username = f"user_{uuid.uuid4().hex[:8]}"

    email = f"{username}@example.com"

    response = client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": "test123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == username

    assert data["email"] == email


def test_login_user(user_factory):

    user = user_factory()

    login_response = client.post(
        "/login",
        data={
            "username": user["username"],
            "password": user["password"]
        }
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"


def test_login_with_invalid_password(user_factory):

    user = user_factory()

    response = client.post(
        "/login",
        data={
            "username": user["username"],
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid username or password"
    }


def test_protected_route(user_factory):

    user = user_factory()

    me_response = client.get(
        "/me",
        headers={
            "Authorization": f"Bearer {user['token']}"
        }
    )

    assert me_response.status_code == 200

    data = me_response.json()

    assert data["username"] == user["username"]

    assert data["email"] == user["email"]


def test_protected_route_without_token():

    response = client.get("/me")

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_me_with_auth_user(auth_user):

    response = client.get(
        "/me",
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == auth_user["username"]

    assert data["email"] == auth_user["email"]