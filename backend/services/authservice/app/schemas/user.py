import uuid
from pydantic import BaseModel,ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=6, max_length=100)

class UserCreate(UserBase):
    name: str = Field(max_length=100)

class UserLogin(UserBase):
    pass

class UserUpdatePWD(BaseModel):
    password: str = Field(min_length=6, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)

class UserResponse(BaseModel):
    id: uuid.UUID = Field(...,description="Unique user identifier")    
    name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=100)
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)