from fastapi import HTTPException, status
from app.api.v1.auth.schemas import UserRegister, UserLogin, UserResponse, Token
from app.api.v1.auth.model import UserModel
from app.api.v1.auth.repository import UserRepository
from app.config.security import hash_password, verify_password, create_access_token

class AuthService:
    @staticmethod
    async def register_user(payload: UserRegister) -> Token:
        existing_user = await UserRepository.get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists."
            )
        
        hashed_pwd = hash_password(payload.password)
        user_doc = UserModel.create_user_document(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed_pwd,
            role=payload.role or "Doctor"
        )
        
        created_doc = await UserRepository.create_user(user_doc)
        user_id = str(created_doc.get("id") or created_doc.get("_id"))
        
        user_resp = UserResponse(
            id=user_id,
            name=created_doc["name"],
            email=created_doc["email"],
            role=created_doc["role"],
            avatar=created_doc.get("avatar"),
            created_at=str(created_doc["created_at"])
        )
        
        token_str = create_access_token(data={"sub": user_id, "email": created_doc["email"]})
        return Token(access_token=token_str, token_type="bearer", user=user_resp)

    @staticmethod
    async def login_user(email: str, password: str) -> Token:
        user_doc = await UserRepository.get_user_by_email(email)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        if not user_doc:
            raise credentials_exception
            
        if not verify_password(password, user_doc["hashed_password"]):
            raise credentials_exception
        
        user_id = str(user_doc.get("id") or user_doc.get("_id"))
        user_resp = UserResponse(
            id=user_id,
            name=user_doc["name"],
            email=user_doc["email"],
            role=user_doc["role"],
            avatar=user_doc.get("avatar"),
            created_at=str(user_doc["created_at"])
        )
        
        token_str = create_access_token(data={"sub": user_id, "email": user_doc["email"]})
        return Token(access_token=token_str, token_type="bearer", user=user_resp)

    @staticmethod
    async def refresh_user_token(current_user: UserResponse) -> Token:
        token_str = create_access_token(data={"sub": current_user.id, "email": current_user.email})
        return Token(access_token=token_str, token_type="bearer", user=current_user)
