import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, and_

from app.models.user import User
from app.core.security import Password

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pwd = Password()
    
    async def get_user_by_id(self, id: uuid.UUID):
        stmt = (
            select(User)
            .where(User.id == id)
        )
        
        result = await self.session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str):
        stmt = (
            select(User)
            .where(User.email == email)
        )
        
        result = await self.session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        stmt = (
            insert(User)
            .values(
                name=name,
                email=email,
                hashed_password=hashed_password
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
    
    async def change_user_to_verified(self, email: str):
        stmt = (
            update(User)
            .values(is_verified=True)
            .where(User.email == email)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def update_password(self, email: str, new_hashed_password: str):
        stmt = (
            update(User)
            .values(hashed_password=new_hashed_password)
            .where(User.email == email)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def delete_user(self, email: str, password: str):
        stmt = (
            delete(User)
            .where(User.email == email)
        )

        await self.session.execute(stmt)
        await self.session.commit()