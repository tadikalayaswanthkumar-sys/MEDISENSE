from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config.security import decode_access_token
from app.api.v1.auth.repository import UserRepository
from app.api.v1.auth.schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")
        
    user_doc = await UserRepository.get_user_by_id(user_id)
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        
    return UserResponse(
        id=user_doc["_id"],
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc["role"],
        avatar=user_doc["avatar"],
        created_at=user_doc["created_at"]
    )
