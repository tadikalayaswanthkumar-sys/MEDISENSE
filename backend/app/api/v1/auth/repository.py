from sqlalchemy import select
from app.config.database import db_instance
from app.db.models import User

class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str) -> dict:
        normalized_email = email.lower().strip()
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                result = await session.execute(
                    select(User).where(User.email == normalized_email)
                )
                user = result.scalar_one_or_none()
                return user.to_dict() if user else None
        else:
            return db_instance.in_memory_store["users"].get(normalized_email)

    @staticmethod
    async def get_user_by_id(user_id: str) -> dict:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                result = await session.execute(
                    select(User).where(User.id == user_id)
                )
                user = result.scalar_one_or_none()
                return user.to_dict() if user else None
        else:
            for u in db_instance.in_memory_store["users"].values():
                if u.get("_id") == user_id or u.get("id") == user_id:
                    return u
            return None

    @staticmethod
    async def create_user(user_doc: dict) -> dict:
        email = user_doc["email"]
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                user = User(
                    id=user_doc.get("_id") or user_doc.get("id"),
                    name=user_doc.get("name"),
                    email=email.lower().strip(),
                    hashed_password=user_doc.get("hashed_password"),
                    role=user_doc.get("role", "Doctor"),
                    avatar=user_doc.get("avatar"),
                    is_active=user_doc.get("is_active", True),
                    created_at=user_doc.get("created_at")
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user.to_dict()
        else:
            db_instance.in_memory_store["users"][email] = user_doc
            return user_doc
