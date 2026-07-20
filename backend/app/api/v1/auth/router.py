from fastapi import APIRouter, Depends, status, Request, HTTPException
from app.api.v1.auth.schemas import UserRegister, UserResponse, Token, MessageResponse
from app.api.v1.auth.service import AuthService
from app.dependencies.current_user import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister):
    """Registers a new user account and returns JWT token."""
    return await AuthService.register_user(payload)

@router.post("/login", response_model=Token)
async def login(request: Request):
    """
    Authenticates user and returns access token.
    Supports both JSON body (React Frontend) and Form Data (Swagger UI Authorize).
    """
    email = None
    password = None

    content_type = request.headers.get("content-type", "")
    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form = await request.form()
        email = form.get("username") or form.get("email")
        password = form.get("password")
    else:
        try:
            body = await request.json()
            email = body.get("email") or body.get("username")
            password = body.get("password")
        except Exception:
            pass

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required for login."
        )

    return await AuthService.login_user(email=str(email), password=str(password))

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Retrieves current authenticated user details."""
    return current_user

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user: UserResponse = Depends(get_current_user)):
    """Logs out user session."""
    return MessageResponse(message="Successfully logged out.")

@router.post("/refresh", response_model=Token)
async def refresh(current_user: UserResponse = Depends(get_current_user)):
    """Refreshes and issues a new JWT access token."""
    return await AuthService.refresh_user_token(current_user)
