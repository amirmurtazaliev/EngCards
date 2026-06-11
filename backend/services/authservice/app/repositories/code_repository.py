from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert

from app.models.code import VerificationCode

class CodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_code_by_email(self, email: str) -> VerificationCode:
        stmt = (
            select(VerificationCode)
            .where(VerificationCode.user_email == email)
            .order_by(VerificationCode.created_at.desc())
            .limit(1)
        )
        
        result = await self.session.execute(stmt)
        
        return result.scalar_one_or_none()

    async def create_code(self, email: str, code: int) -> VerificationCode:
        stmt = (
            insert(VerificationCode)
            .values(
                user_email=email,
                code=code
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit() 