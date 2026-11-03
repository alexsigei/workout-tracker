# Workout Tracker API

A Flask REST API for managing personal workouts. Users can create an account, log in, and manage their workout records securely.

## Features

- User registration and JWT authentication.
- Secure password hashing with Flask-Bcrypt.
- Create, view, update, and delete workouts.
- Paginated workout listing.
- User-specific workout access.
- SQLite database with Flask-Migrate.
- Automated tests with pytest.

## Technologies

Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-JWT-Extended, SQLite, and pytest.

## Setup

Clone the repository:

```bash
git clone https://github.com/alexsigei/workout-tracker.git
cd workout-tracker
```

Install dependencies:

```bash
pipenv install --dev
```

## Database

Apply the existing migrations:

```bash
pipenv run flask --app app db upgrade
```

To populate the database with sample users and workouts:

```bash
pipenv run python seed.py
```

**Note:** The seed script clears existing users and workouts before inserting sample data. Use it only when you are comfortable resetting the database.

## Running the Application

Start the development server:

```bash
pipenv run flask --app app run --debug
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a user |
| POST | `/login` | Log in and receive a JWT |
| GET | `/me` | Get the authenticated user |
| POST | `/workouts` | Create a workout |
| GET | `/workouts` | List workouts |
| GET | `/workouts/<id>` | Get a specific workout |
| PATCH | `/workouts/<id>` | Update a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Authentication

Protected endpoints require a JWT access token in the request header:

```http
Authorization: Bearer <access_token>
```

Obtain a token by sending a POST request to `/login` with a username and password.

## Running Tests

Run the test suite:

```bash
pipenv run pytest
```

## Sample Login Credentials

After running the seed script:

| Username | Password |
|---|---|
| alex | password123 |
| jane | password123 |
