import sys
import os
import uuid

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pytest

from fastapi.testclient import TestClient

from tests.database import (
    TestingSessionLocal
)

from app.database.dependencies import (
    get_db
)

from app.main import app

from app.database.database import Base
from tests.database import engine
    


@pytest.fixture(
    scope="session",
    autouse=True
)
def setup_database():

    Base.metadata.create_all(
        bind=engine
    )

    yield

    Base.metadata.drop_all(
        bind=engine
    )

def override_get_db():

    print("USING TEST DATABASE")

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def _register_and_login():

    username = f"user_{uuid.uuid4().hex[:8]}"

    email = f"{username}@example.com"

    password = "test123"

    client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    login_response = client.post(
        "/login",
        data={
            "username": username,
            "password": password
        }
    )

    token = login_response.json()["access_token"]

    return {
        "username": username,
        "email": email,
        "password": password,
        "token": token
    }


@pytest.fixture
def user_factory():

    def create_user():
        return _register_and_login()

    return create_user


@pytest.fixture
def auth_token(user_factory):

    return user_factory()["token"]


@pytest.fixture
def auth_user():

    return _register_and_login()


@pytest.fixture
def test_task(auth_user):

    response = client.post(
        "/tasks",
        json={
            "title": "Fixture Task",
            "description": "Created by fixture",
            "completed": False
        },
        headers={
            "Authorization":
            f"Bearer {auth_user['token']}"
        }
    )

    task = response.json()

    return {
        "task": task,
        "user": auth_user
    }