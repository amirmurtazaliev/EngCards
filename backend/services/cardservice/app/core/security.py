from dataclasses import dataclass

import jwt
from flask import request
from werkzeug.exceptions import Unauthorized

from app.core.config import settings


@dataclass(frozen=True)
class AuthUser:
    id: str
    email: str | None = None


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Access token expired")
    except jwt.PyJWTError:
        raise Unauthorized("Invalid token")

    if payload.get("type") != "access":
        raise Unauthorized("Invalid token type")

    return payload


def get_current_user() -> AuthUser:
    token = request.cookies.get(settings.access_cookie_name)

    if not token:
        raise Unauthorized("No token")

    payload = decode_access_token(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise Unauthorized("Invalid token")

    return AuthUser(id=str(user_id), email=payload.get("email"))