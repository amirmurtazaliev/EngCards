import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CardCreate(BaseModel):
    english_word: str = Field(min_length=1, max_length=120)
    russian_word: str = Field(min_length=1, max_length=120)


class CardResponse(CardCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)