from fastapi import APIRouter, Depends, status
from app.api.v1.auth.schemas import UserRegister, UserLogin, UserResponse, Token
from app.api.v1.auth.service import AuthService
from app.dependencies.current_user import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    return await AuthService.register_user(payload)

@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    return await AuthService.login_user(payload)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
