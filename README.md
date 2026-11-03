# Workout Tracker API

A Flask REST API for managing personal workout records. Users can create accounts, log in, and manage their workouts securely.

### Features
- User registration and JWT authentication.
- Secure password hashing with Flask-Bcrypt.
- Create, retrieve, update, and delete workouts.
- User-specific workout access.
- Paginated workout listings.
- Database migrations and sample data seeding.

### Built With
Python · Flask · Flask-SQLAlchemy · SQLite · Flask-Bcrypt · Flask-JWT-Extended · Flask-Migrate · Pytest

### Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd workout-tracker
```

Install dependencies:

```bash
pipenv install --dev
```

Initialize the database:

```bash
pipenv run flask --app app db upgrade
```

Load sample data:

```bash
pipenv run python seed.py
```

Start the server:

```bash
pipenv run flask --app app run --debug
```

The API runs at `http://127.0.0.1:5000`.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a user |
| POST | `/login` | Log in and receive an access token |
| GET | `/me` | Get the authenticated user |
| GET | `/workouts` | List workouts |
| GET | `/workouts/<id>` | Get a workout |
| POST | `/workouts` | Create a workout |
| PATCH | `/workouts/<id>` | Update a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

Workout endpoints require a JWT access token in the `Authorization` header:

```text
Authorization: Bearer <access_token>
```

### Running Tests

```bash
pipenv run pytest
```

### Sample Accounts

| Username | Password |
|---|---|
| alex | password123 |
| jane | password123 |

Sample accounts are created by running the seed script.