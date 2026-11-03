import pytest

from app import create_app
from extensions import db


@pytest.fixture
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "JWT_SECRET_KEY": "test-secret-key-that-is-at-least-32-characters"
    })

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def authenticated_user(client):
    client.post("/signup", json={
        "username": "testuser",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = client.post("/login", json={
        "username": "testuser",
        "password": "password123"
    })

    token = response.json["token"]

    return {
        "headers": {
            "Authorization": f"Bearer {token}"
        },
        "user_id": 1
    }
