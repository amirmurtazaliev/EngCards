import asyncio

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.api.v1.card import card_blueprint
from app.core.config import settings
from app.db.database import init_db
from app.models.card import Card


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        APP_NAME=settings.app_name,
        DEBUG=settings.debug,
        JSON_SORT_KEYS=False,
    )

    CORS(
        app,
        origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        supports_credentials=True,
        methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    register_error_handlers(app)
    app.register_blueprint(card_blueprint)

    @app.get("/")
    def root():
        return jsonify({"message": "Welcome to EngCards card service!"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    with app.app_context():
        asyncio.run(init_db())

    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValueError)
    def value_error_handler(exc: ValueError):
        return jsonify({"detail": str(exc)}), 400

    @app.errorhandler(HTTPException)
    def http_exception_handler(exc: HTTPException):
        return jsonify({"detail": exc.description}), exc.code


app = create_app()