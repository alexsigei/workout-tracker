from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from models import User, Workout
from resources.auth import auth_bp
from resources.workouts import workouts_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Apply test settings before initializing extensions.
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(workouts_bp)

    @app.route("/")
    def home():
        return {"message": "Workout Tracker API is running"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
