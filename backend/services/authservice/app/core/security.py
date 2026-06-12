import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Literal

from flask import request
from werkzeug.exceptions import Forbidden, Unauthorized

from app.core.config import settings


@dataclass
class AuthUser:
    id: str
    email: str
    is_verified: bool

def create_token(
    user: AuthUser,
    expires_delta: timedelta,
) -> str:
    expires_at = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": str(user.id),
        "user_id": str(user.id),
        "email": user.email,
        "is_verified": user.is_verified,
        "type": "access",
        "exp": expires_at,
    }

    return jwt.encode(payload, settings.secret, settings.algorithm)



def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
       raise Unauthorized("token expired")
    except jwt.PyJWTError:
        raise Unauthorized("Invalid token")

    return payload

def decode_access_token(token: str) -> dict:
    return decode_token(token, expected_type="access")


def get_current_user() -> AuthUser:   
    token = request.cookies.get(settings.access_cookie_name)
    
    if not token:
        raise Unauthorized("No token")

    
    payload = decode_token(token)
    user_id = payload.get("user_id")
    
    if not user_id:
        raise Unauthorized("Invalid token")
    
    return AuthUser(
        id=user_id,
        email=payload.get("email"),
        is_verified=payload.get("is_verified"),
    )
    
def require_verified_user(user: AuthUser | None = None) -> AuthUser:
    user = user or get_current_user()
    if not user.is_verified:
        raise Forbidden("Email is not verified")
    return user
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Password:
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)