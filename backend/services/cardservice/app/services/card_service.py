import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.exceptions import NotFound

from app.repositories.card_repository import CardRepository


class CardService:
    def __init__(self, session: AsyncSession):
        self.card_repository = CardRepository(session)

    async def list_cards(self, user_id: str):
        return await self.card_repository.list_cards(uuid.UUID(user_id))

    async def create_card(self, user_id: str, english_word: str, russian_word: str):
        return await self.card_repository.create_card(
            user_id=uuid.UUID(user_id),
            english_word=english_word.strip(),
            russian_word=russian_word.strip(),
        )

    async def delete_card(self, user_id: str, card_id: str) -> dict[str, str]:
        deleted = await self.card_repository.delete_card(
            user_id=uuid.UUID(user_id),
            card_id=uuid.UUID(card_id),
        )

        if not deleted:
            raise NotFound("Card not found")

        return {"message": "Card deleted"}