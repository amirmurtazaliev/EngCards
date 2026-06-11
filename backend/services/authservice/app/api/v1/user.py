from flask import Blueprint, jsonify, make_response, request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from app.core.config import settings
from app.core.security import (
    get_current_user,
    require_verified_user,
)
from app.db.database import SessionLocal
from app.schemas.user import UserBase, UserCreate, UserUpdatePWD
from app.services.user_service import UserService

user_blueprint = Blueprint("user", __name__, url_prefix="/api/v1/user")


def _json_body():
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequest("Request body must be valid JSON")
    return data


def _validation_error_response(exc: ValidationError):
    return jsonify({"detail": exc.errors()}), 422


@user_blueprint.post("/login")
async def login():
    try:
        user_data = UserBase.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        service = UserService(session)
        user = await service.get_user(user_data.email, user_data.password)

    response = make_response(jsonify({"msg": "you are loggined"}))
    service.set_auth_cookies(response, user)
    return response

@user_blueprint.post("/register")
async def register():
    try:
        user_data = UserCreate.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        service = UserService(session)
        await service.register_user(**user_data.model_dump())
        user = await service.get_user(user_data.email, user_data.password)

    response = make_response(jsonify({"msg": "you are regitred"}))
    service.set_auth_cookies(response, user)
    
    return response

@user_blueprint.post("/logout")
def logout():
    response = make_response(jsonify({"message": "Successfully logged out"}))
    response.delete_cookie(settings.access_cookie_name)
    return response


@user_blueprint.patch("/update/password")
async def update_password():
    user_data = require_verified_user(get_current_user())

    try:
        pwds_data = UserUpdatePWD.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        service = UserService(session)
        result = await service.update_password(user_data.email, **pwds_data.model_dump())

    return jsonify(result)


@user_blueprint.delete("/delete")
async def delete_user():
    try:
        user_data = UserBase.model_validate(_json_body())
    except ValidationError as exc:
        return _validation_error_response(exc)

    async with SessionLocal() as session:
        service = UserService(session)
        result = await service.delete_user(user_data.email, user_data.password)

    return jsonify(result)