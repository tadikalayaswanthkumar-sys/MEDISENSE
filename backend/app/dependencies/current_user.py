from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config.security import decode_access_token
from app.api.v1.auth.repository import UserRepository
from app.api.v1.auth.schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise credentials_exception
        
    user_doc = await UserRepository.get_user_by_id(user_id)
    if not user_doc:
        raise credentials_exception
        
    return UserResponse(
        id=str(user_doc.get("id") or user_doc.get("_id")),
        name=user_doc["name"],
        email=user_doc["email"],
        role=user_doc["role"],
        avatar=user_doc.get("avatar"),
        created_at=str(user_doc["created_at"])
    )
