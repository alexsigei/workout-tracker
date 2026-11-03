
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Workout


workouts_bp = Blueprint("workouts", __name__)


def workout_to_dict(workout):
    """Convert a Workout object into a dictionary."""
    return {
        "id": workout.id,
        "name": workout.name,
        "exercise_type": workout.exercise_type,
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "created_at": (
            workout.created_at.isoformat()
            if workout.created_at else None
        ),
        "user_id": workout.user_id
    }


def get_owned_workout(workout_id, user_id):
    """Find a workout belonging to the authenticated user."""
    return Workout.query.filter_by(
        id=workout_id,
        user_id=user_id
    ).first()


@workouts_bp.route("/workouts", methods=["GET"])
@jwt_required()
def get_workouts():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1:
        return {"error": "Page and per_page must be positive"}, 400

    per_page = min(per_page, 100)

    pagination = Workout.query.filter_by(
        user_id=user_id
    ).order_by(
        Workout.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "workouts": [
            workout_to_dict(workout)
            for workout in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    }, 200


@workouts_bp.route("/workouts/<int:workout_id>", methods=["GET"])
@jwt_required()
def get_workout(workout_id):
    user_id = int(get_jwt_identity())

    workout = get_owned_workout(workout_id, user_id)

    if not workout:
        return {"error": "Workout not found"}, 404

    return workout_to_dict(workout), 200


@workouts_bp.route("/workouts", methods=["POST"])
@jwt_required()
def create_workout():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    exercise_type = data.get("exercise_type")
    duration = data.get("duration_minutes")
    notes = data.get("notes")

    if not isinstance(name, str) or not name.strip():
        return {"error": "Workout name is required"}, 400

    if not isinstance(exercise_type, str) or not exercise_type.strip():
        return {"error": "Exercise type is required"}, 400

    if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
        return {"error": "Duration must be a positive integer"}, 400

    if notes is not None and not isinstance(notes, str):
        return {"error": "Notes must be text"}, 400

    workout = Workout(
        name=name.strip(),
        exercise_type=exercise_type.strip(),
        duration_minutes=duration,
        notes=notes,
        user_id=user_id
    )

    db.session.add(workout)
    db.session.commit()

    return {
        "message": "Workout created successfully",
        "workout": workout_to_dict(workout)
    }, 201


@workouts_bp.route("/workouts/<int:workout_id>", methods=["PATCH"])
@jwt_required()
def update_workout(workout_id):
    user_id = int(get_jwt_identity())

    workout = get_owned_workout(workout_id, user_id)

    if not workout:
        return {"error": "Workout not found"}, 404

    data = request.get_json(silent=True) or {}

    allowed_fields = {
        "name",
        "exercise_type",
        "duration_minutes",
        "notes"
    }

    if not data or not set(data).issubset(allowed_fields):
        return {"error": "Provide valid workout fields to update"}, 400

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return {"error": "Workout name cannot be empty"}, 400
        workout.name = data["name"].strip()

    if "exercise_type" in data:
        if not isinstance(data["exercise_type"], str) or not data["exercise_type"].strip():
            return {"error": "Exercise type cannot be empty"}, 400
        workout.exercise_type = data["exercise_type"].strip()

    if "duration_minutes" in data:
        duration = data["duration_minutes"]
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            return {"error": "Duration must be a positive integer"}, 400
        workout.duration_minutes = duration

    if "notes" in data:
        if data["notes"] is not None and not isinstance(data["notes"], str):
            return {"error": "Notes must be text"}, 400
        workout.notes = data["notes"]

    db.session.commit()

    return {
        "message": "Workout updated successfully",
        "workout": workout_to_dict(workout)
    }, 200


@workouts_bp.route("/workouts/<int:workout_id>", methods=["DELETE"])
@jwt_required()
def delete_workout(workout_id):
    user_id = int(get_jwt_identity())

    workout = get_owned_workout(workout_id, user_id)

    if not workout:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()

    return {"message": "Workout deleted successfully"}, 200
