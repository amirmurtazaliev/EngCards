from pydantic import BaseModel, Field, EmailStr, ConfigDict

class VerificationBase(BaseModel):
    email: EmailStr = Field(max_length=100)
    
class VerificationCreate(VerificationBase):
    code: int

class VerificationResponse(VerificationCreate):
    pass

    model_config = ConfigDict(from_attributes=True)