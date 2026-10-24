from flask import Flask, jsonify

from config import Config
from .extensions import db, migrate
from .routes import api_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/")
    def health_check():
        return jsonify({"message": "Workout API is running"}), 200

    return app
