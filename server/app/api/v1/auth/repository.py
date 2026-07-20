from app.config.database import db_instance

class UserRepository:
    @staticmethod
    async def get_user_by_email(email: str) -> dict:
        normalized_email = email.lower().strip()
        if db_instance.is_connected and db_instance.db is not None:
            return await db_instance.db.users.find_one({"email": normalized_email})
        else:
            return db_instance.in_memory_store["users"].get(normalized_email)

    @staticmethod
    async def get_user_by_id(user_id: str) -> dict:
        if db_instance.is_connected and db_instance.db is not None:
            return await db_instance.db.users.find_one({"_id": user_id})
        else:
            for u in db_instance.in_memory_store["users"].values():
                if u.get("_id") == user_id:
                    return u
            return None

    @staticmethod
    async def create_user(user_doc: dict) -> dict:
        email = user_doc["email"]
        if db_instance.is_connected and db_instance.db is not None:
            await db_instance.db.users.insert_one(user_doc)
            return user_doc
        else:
            db_instance.in_memory_store["users"][email] = user_doc
            return user_doc
