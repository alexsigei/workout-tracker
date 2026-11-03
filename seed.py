
from app import app
from extensions import db
from models import User, Workout


def seed_data():
    with app.app_context():
        # Clear existing sample data
        Workout.query.delete()
        User.query.delete()

        # Create sample users
        users = [
            User(username="alex"),
            User(username="jane")
        ]

        users[0].set_password("password123")
        users[1].set_password("password123")

        db.session.add_all(users)
        db.session.commit()

        # Create sample workouts
        workouts = [
            Workout(
                name="Morning Run",
                exercise_type="Cardio",
                duration_minutes=30,
                notes="Easy morning run",
                user_id=users[0].id
            ),
            Workout(
                name="Weight Training",
                exercise_type="Strength",
                duration_minutes=45,
                notes="Upper body workout",
                user_id=users[0].id
            ),
            Workout(
                name="Evening Swim",
                exercise_type="Swimming",
                duration_minutes=40,
                notes="Practised freestyle",
                user_id=users[0].id
            ),
            Workout(
                name="Yoga Session",
                exercise_type="Flexibility",
                duration_minutes=50,
                notes="Full body stretching",
                user_id=users[1].id
            ),
            Workout(
                name="Cycling",
                exercise_type="Cardio",
                duration_minutes=60,
                notes="Outdoor cycling",
                user_id=users[1].id
            ),
            Workout(
                name="Leg Day",
                exercise_type="Strength",
                duration_minutes=45,
                notes="Lower body workout",
                user_id=users[1].id
            )
        ]

        db.session.add_all(workouts)
        db.session.commit()

        print("Database seeded successfully!")
        print(f"Created {len(users)} users.")
        print(f"Created {len(workouts)} workouts.")


if __name__ == "__main__":
    seed_data()
