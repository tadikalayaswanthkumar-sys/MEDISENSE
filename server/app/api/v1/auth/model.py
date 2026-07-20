from datetime import datetime, timezone
import uuid

class UserModel:
    @staticmethod
    def create_user_document(name: str, email: str, hashed_password: str, role: str = "Doctor", avatar: str = None) -> dict:
        return {
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": email.lower().strip(),
            "hashed_password": hashed_password,
            "role": role,
            "avatar": avatar or "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150&auto=format&fit=crop&q=80",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
