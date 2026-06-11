import asyncio
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import *
from app.integrations.http_client import NotifyHTTPClient
from app.core.config import settings
from app.core.exceptions import VerificationCodeExpiredError, VerificationCodeInvalidError
from app.models.code import VerificationCode

class CodeService:
    def __init__(self, session: AsyncSession, notify_client: NotifyHTTPClient):
        self.code_db = CodeRepository(session)
        self.user_db = UserRepository(session)
        self.http_client = notify_client
    
    @staticmethod
    def check_code_to_valid(code_from_user: int, code_data: VerificationCode):
        now = datetime.now(timezone.utc)
        
        if code_data.created_at.tzinfo is None:
            created_at = code_data.created_at.replace(tzinfo=timezone.utc)
        else:
            created_at = code_data.created_at
        
        diff = now - created_at
        
        if code_from_user != code_data.code:
            raise VerificationCodeInvalidError("The verification code you entered is incorrect")
        
        if diff >= timedelta(minutes=10):
            raise VerificationCodeExpiredError("Verification code has expired. Please request a new one")
    
    @staticmethod
    def collect_data_to_send(email: str, code: int):
        data_to_send = {
            "sender_name": settings.app_name,
            "recipient_email": email,
            "message": str(code),
        }
        
        return data_to_send
    
    async def create_code(self, email: str):
        code = random.randint(1000, 9999)
        
        await self.code_db.create_code(email, code)
        
        return code
    
    async def send_verification_code(self, email: str, max_retries: int):
        code = await self.create_code(email)
        
        data_to_send = self.collect_data_to_send(email, code)
        
        
        attempts = max_retries
        last_response = None
        
        for attempt in range(attempts):
            response = await self.http_client.send_post_request("sendmsg", data_to_send)
        
            last_response = response
            
            if response.status not in settings.retry_statuses:
                break
            
            if attempt < attempts:
                await asyncio.sleep(0.2 * (attempt + 1))
            
            
        return last_response.data
        
    async def check_code(self, email: str, code: int):
        code_data = await self.code_db.get_code_by_email(email)
        
        if not code_data:
            raise VerificationCodeInvalidError("Verification code not found")

        self.check_code_to_valid(code, code_data)
        
        return await self.user_db.change_user_to_verified(email)
        
    
    