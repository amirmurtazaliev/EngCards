import uuid

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card


class CardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_cards(self, user_id: uuid.UUID) -> list[Card]:
        stmt = select(Card).where(Card.user_id == user_id).order_by(Card.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_card(self, user_id: uuid.UUID, english_word: str, russian_word: str) -> Card:
        stmt = (
            insert(Card)
            .values(
                user_id=user_id,
                english_word=english_word,
                russian_word=russian_word,
            )
            .returning(Card)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def delete_card(self, user_id: uuid.UUID, card_id: uuid.UUID) -> bool:
        stmt = delete(Card).where(Card.id == card_id, Card.user_id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0