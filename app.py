from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from models import User, Workout


def create_app():
    app = Flask(__name__)

    # Load application configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route("/")
    def home():
        return {"message": "Workout Tracker API is running"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
