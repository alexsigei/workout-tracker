
def test_create_workout(client, authenticated_user):
    response = client.post(
        "/workouts",
        json={
            "name": "Morning Run",
            "exercise_type": "Cardio",
            "duration_minutes": 30,
            "notes": "Easy morning run"
        },
        headers=authenticated_user["headers"]
    )

    assert response.status_code == 201
    assert response.json["workout"]["name"] == "Morning Run"


def test_get_workouts(client, authenticated_user):
    client.post(
        "/workouts",
        json={
            "name": "Morning Run",
            "exercise_type": "Cardio",
            "duration_minutes": 30
        },
        headers=authenticated_user["headers"]
    )

    response = client.get(
        "/workouts",
        headers=authenticated_user["headers"]
    )

    assert response.status_code == 200
    assert len(response.json["workouts"]) == 1


def test_update_workout(client, authenticated_user):
    headers = authenticated_user["headers"]

    create_response = client.post(
        "/workouts",
        json={
            "name": "Morning Run",
            "exercise_type": "Cardio",
            "duration_minutes": 30
        },
        headers=headers
    )

    workout_id = create_response.json["workout"]["id"]

    response = client.patch(
        f"/workouts/{workout_id}",
        json={"duration_minutes": 60},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["workout"]["duration_minutes"] == 60


def test_delete_workout(client, authenticated_user):
    headers = authenticated_user["headers"]

    create_response = client.post(
        "/workouts",
        json={
            "name": "Morning Run",
            "exercise_type": "Cardio",
            "duration_minutes": 30
        },
        headers=headers
    )

    workout_id = create_response.json["workout"]["id"]

    response = client.delete(
        f"/workouts/{workout_id}",
        headers=headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/workouts/{workout_id}",
        headers=headers
    )

    assert get_response.status_code == 404


def test_workouts_require_authentication(client):
    response = client.get("/workouts")

    assert response.status_code == 401


def test_user_cannot_access_another_users_workout(
    client,
    authenticated_user
):
    headers = authenticated_user["headers"]

    create_response = client.post(
        "/workouts",
        json={
            "name": "Private Workout",
            "exercise_type": "Strength",
            "duration_minutes": 45
        },
        headers=headers
    )

    workout_id = create_response.json["workout"]["id"]

    # Create and authenticate a second user
    client.post("/signup", json={
        "username": "anotheruser",
        "password": "password123",
        "password_confirmation": "password123"
    })

    login_response = client.post("/login", json={
        "username": "anotheruser",
        "password": "password123"
    })

    other_headers = {
        "Authorization": (
            f"Bearer {login_response.json['token']}"
        )
    }

    response = client.get(
        f"/workouts/{workout_id}",
        headers=other_headers
    )

    assert response.status_code == 404
