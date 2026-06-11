import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import *
from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import Password, create_token
from app.core.config import settings

class UserService:
    def __init__(self, session: AsyncSession):
        self.user_db = UserRepository(session)
        self.code_db = CodeRepository(session)
        self.pwd_acts = Password()
    
    def set_auth_cookies(self, response, user) -> None:
        access_token = create_token(user)

        response.set_cookie(
            key=settings.access_cookie_name,
            value=access_token,
            httponly=True,
            secure=settings.cookie_secure,
            samesite="lax",
            path="/",
            max_age=settings.access_token_expire_minutes * 60,
        )
    
    async def get_user(self, email: str, password: str):
        user = await self.user_db.get_user_by_email(email)
        
        if not user or not self.pwd_acts.verify_password(password, user.hashed_password):
            raise UserNotFoundError("user not found")

        return user
    
    async def get_user_by_id(self, id: uuid.UUID):
        user = await self.user_db.get_user_by_id(id)
        
        if not user:
            raise UserNotFoundError("user not found")
        
        return user

    async def register_user(self, name: str, email: str, password: str):
        existing_user = await self.user_db.get_user_by_email(email)
        
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {email} already exists")
        
        hashed_password = self.pwd_acts.get_password_hash(password)
        
        return await self.user_db.create_user(name, email, hashed_password)
    
    async def update_password(self, email: str, password: str, new_password: str):
        user = await self.user_db.get_user_by_email(email)
        
        if not user:
            raise UserNotFoundError("User not found")
        
        if not self.pwd_acts.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("incorrect email or password")
        
        new_hashed_password = self.pwd_acts.get_password_hash(new_password)
        
        return await self.user_db.update_password(email, new_hashed_password)
        
    async def delete_user(self, email: str, password: str):
        user = await self.user_db.get_user_by_email(email)
        if not user:
            raise UserNotFoundError("User not found")

        if not self.pwd_acts.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("incorrect email or password")

        return await self.user_db.delete_user(email, password)