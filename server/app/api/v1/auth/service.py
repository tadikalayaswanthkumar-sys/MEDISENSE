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
                detail="User with this email already exists."
            )
        
        hashed_pwd = hash_password(payload.password)
        user_doc = UserModel.create_user_document(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed_pwd,
            role=payload.role
        )
        
        created_doc = await UserRepository.create_user(user_doc)
        
        user_resp = UserResponse(
            id=created_doc["_id"],
            name=created_doc["name"],
            email=created_doc["email"],
            role=created_doc["role"],
            avatar=created_doc["avatar"],
            created_at=created_doc["created_at"]
        )
        
        token_str = create_access_token(data={"sub": created_doc["_id"], "email": created_doc["email"]})
        return Token(access_token=token_str, user=user_resp)

    @staticmethod
    async def login_user(payload: UserLogin) -> Token:
        user_doc = await UserRepository.get_user_by_email(payload.email)
        if not user_doc or not verify_password(payload.password, user_doc["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password credentials."
            )
        
        user_resp = UserResponse(
            id=user_doc["_id"],
            name=user_doc["name"],
            email=user_doc["email"],
            role=user_doc["role"],
            avatar=user_doc["avatar"],
            created_at=user_doc["created_at"]
        )
        
        token_str = create_access_token(data={"sub": user_doc["_id"], "email": user_doc["email"]})
        return Token(access_token=token_str, user=user_resp)
