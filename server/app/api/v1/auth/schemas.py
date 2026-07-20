from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, example="Dr. Alex Vance")
    email: EmailStr = Field(..., example="alex.vance@medisense.ai")
    password: str = Field(..., min_length=6, example="Secret123!")
    role: Optional[str] = Field("Doctor", example="Doctor")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="alex.vance@medisense.ai")
    password: str = Field(..., example="Secret123!")

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    avatar: Optional[str] = None
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
