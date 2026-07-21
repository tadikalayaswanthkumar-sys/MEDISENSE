from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserRegister(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"name": "Alex Vance", "email": "alex.vance@medisense.ai", "password": "Secret123!", "role": "User"}})
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Optional[str] = Field("User")

class UserLogin(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"email": "alex.vance@medisense.ai", "password": "Secret123!"}})
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str = "User"
    avatar: Optional[str] = None
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class MessageResponse(BaseModel):
    message: str
