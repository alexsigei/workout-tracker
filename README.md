# Workout Tracker API

A RESTful API built with Flask that allows users to register, authenticate, and manage their personal workout records. JWT authentication protects the API and ensures users can only access their own data.

## Features

- User registration and login.
- Secure password hashing with Flask-Bcrypt.
- JWT-based authentication.
- Create, retrieve, update, and delete workouts.
- User-specific workout records.
- Paginated workout listings.
- Database migrations with Flask-Migrate.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-JWT-Extended
- Flask-Migrate
- SQLite
- Pytest

## Installation

Clone the repository:

```bash
git clone https://github.com/alexsigei/workout-tracker.git
cd workout-tracker
```

Install dependencies:

```bash
pipenv install --dev
```

## Database Setup

Apply the database migrations:

```bash
pipenv run flask --app app db upgrade
```

Add sample users and workouts:

```bash
pipenv run python seed.py
```

**Note:** The seed script clears existing users and workouts before inserting sample data.

## Running the API

Start the development server:

```bash
pipenv run flask --app app run
```

The API will be available at `http://127.0.0.1:5000`.

To use the supplied JWT frontend client, start the backend on port `5555`:

```bash
pipenv run flask --app app run --port 5555
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a new user |
| POST | `/login` | Authenticate and receive a JWT |
| GET | `/me` | Retrieve the authenticated user's details |

### Workouts

All workout endpoints require a valid JWT.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Retrieve the user's workouts |
| POST | `/workouts` | Create a workout |
| GET | `/workouts/<id>` | Retrieve a specific workout |
| PATCH | `/workouts/<id>` | Update a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Authentication

Include the access token in the request header when accessing protected endpoints:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The workout listing endpoint supports pagination through the `page` and `per_page` query parameters.

Example:

```http
GET /workouts?page=1&per_page=10
```

## Sample Accounts

The seed script creates two accounts:

| Username | Password |
|---|---|
| alex | password123 |
| jane | password123 |

## Running Tests

Run the automated test suite:

```bash
pipenv run pytest -v
```
