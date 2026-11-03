
def test_signup_successfully(client):
    response = client.post("/signup", json={
        "username": "alex",
        "password": "password123"
    })

    assert response.status_code == 201
    assert response.json["user"]["username"] == "alex"


def test_signup_rejects_duplicate_username(client):
    client.post("/signup", json={
        "username": "alex",
        "password": "password123"
    })

    response = client.post("/signup", json={
        "username": "alex",
        "password": "anotherpassword"
    })

    assert response.status_code == 409


def test_signup_rejects_short_password(client):
    response = client.post("/signup", json={
        "username": "alex",
        "password": "123"
    })

    assert response.status_code == 400


def test_login_successfully(client):
    client.post("/signup", json={
        "username": "alex",
        "password": "password123"
    })

    response = client.post("/login", json={
        "username": "alex",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_rejects_wrong_password(client):
    client.post("/signup", json={
        "username": "alex",
        "password": "password123"
    })

    response = client.post("/login", json={
        "username": "alex",
        "password": "wrongpassword"
    })

    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/me")

    assert response.status_code == 401


def test_me_returns_authenticated_user(client, authenticated_user):
    response = client.get(
        "/me",
        headers=authenticated_user["headers"]
    )

    assert response.status_code == 200
    assert response.json["username"] == "testuser"
