import asyncio

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.api.v1 import *
from app.core.config import settings
from app.core.exceptions import (
    DomainError,
    InvalidCredentialsError,
    NotificationServiceError,
    NotificationServiceTimeoutError,
    NotificationServiceUnavailableError,
    UserAlreadyExistsError,
    UserNotFoundError,
    VerificationCodeError,
)
from app.db.database import init_db
from app.models.user import User
from app.models.code import VerificationCode

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        APP_NAME=settings.app_name,
        DEBUG=settings.debug,
        JSON_SORT_KEYS=False,
    )

    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        supports_credentials=True,
        methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.config["MAX_RETRIES"] = settings.notify_max_retries

    register_error_handlers(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(verification_blueprint)

    @app.get("/")
    def root():
        return jsonify(
            {
                "message": "Welcome to flask auth service!",
                "docs": None,
            }
        )

    with app.app_context():
        asyncio.run(init_db())

    return app

def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(DomainError)
    def domain_exception_handler(exc: DomainError):
        if isinstance(exc, UserAlreadyExistsError):
            status_code = 409
        elif isinstance(exc, UserNotFoundError):
            status_code = 404
        elif isinstance(exc, (InvalidCredentialsError, VerificationCodeError)):
            status_code = 400
        else:
            status_code = 500

        return jsonify({"detail": exc.message}), status_code

    @app.errorhandler(NotificationServiceError)
    def notify_exception_handler(exc: NotificationServiceError):
        if isinstance(exc, NotificationServiceTimeoutError):
            status_code = 504
        elif isinstance(exc, NotificationServiceUnavailableError):
            status_code = 503
        else:
            status_code = 500

        return jsonify({"detail": exc.message}), status_code

    @app.errorhandler(HTTPException)
    def http_exception_handler(exc: HTTPException):
        return jsonify({"detail": exc.description}), exc.code

app = create_app()