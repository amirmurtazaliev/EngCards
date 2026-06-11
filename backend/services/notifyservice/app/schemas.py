from pydantic import BaseModel, Field, EmailStr

class Base(BaseModel):
    pass

class MessageData(Base):
    sender_name: str = Field(max_length=100)
    recipient_email: EmailStr = Field(max_length=100)
    message: str = Field(max_length=300)