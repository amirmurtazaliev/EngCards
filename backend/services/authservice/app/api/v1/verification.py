from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from app.db.database import SessionLocal
from app.integrations.http_client import NotifyHTTPClient
from app.schemas.verification import VerificationBase, VerificationCreate
from app.services.verifiaction_service import CodeService

verification_blueprint = Blueprint("verifyemail", __name__, url_prefix="/api/v1/user")


def _json_body():
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequest("Request body must be valid JSON")
    return data


def _validation_error_response(exc: ValidationError):
    return jsonify({"detail": exc.errors()}), 422


@verification_blueprint.post("/send_verification_code")
async def send_verification_code():
    try:
        data = VerificationBase.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        notify_client = NotifyHTTPClient()
        service = CodeService(session, notify_client)
        result = await service.send_verification_code(
            **data.model_dump(),
            max_retries=current_app.config["MAX_RETRIES"],
        )

    return jsonify(result)


@verification_blueprint.post("/verify_email")
async def verify_email():
    try:
        data = VerificationCreate.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        notify_client = NotifyHTTPClient()
        service = CodeService(session, notify_client)
        result = await service.check_code(**data.model_dump())

        return jsonify(result)