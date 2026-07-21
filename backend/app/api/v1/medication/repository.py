from sqlalchemy import select, delete
from app.config.database import db_instance
from app.db.models import Medicine, ReminderHistory

class MedicationRepository:
    @staticmethod
    async def create_medicine(med_doc: dict) -> dict:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                med_id = med_doc.get("_id") or med_doc.get("id")
                medicine = Medicine(
                    id=med_id,
                    user_id=med_doc["user_id"],
                    name=med_doc["name"],
                    dosage=med_doc["dosage"],
                    frequency=med_doc["frequency"],
                    times=med_doc.get("times", []),
                    instructions=med_doc.get("instructions", ""),
                    is_active=med_doc.get("is_active", True),
                    created_at=med_doc.get("created_at")
                )
                session.add(medicine)
                await session.commit()
                await session.refresh(medicine)
                return medicine.to_dict()
        else:
            if "medicines" not in db_instance.in_memory_store:
                db_instance.in_memory_store["medicines"] = {}
            db_instance.in_memory_store["medicines"][med_doc["_id"]] = med_doc
            return med_doc

    @staticmethod
    async def get_user_medicines(user_id: str) -> list:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                result = await session.execute(
                    select(Medicine)
                    .where(Medicine.user_id == user_id, Medicine.is_active == True)
                    .limit(100)
                )
                medicines = result.scalars().all()
                return [m.to_dict() for m in medicines]
        else:
            if "medicines" not in db_instance.in_memory_store:
                return []
            return [m for m in db_instance.in_memory_store["medicines"].values() if m.get("user_id") == user_id and m.get("is_active", True)]

    @staticmethod
    async def delete_medicine_by_id(med_id: str, user_id: str) -> bool:
        """Deletes or deactivates a prescription medicine for a user."""
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                await session.execute(
                    delete(ReminderHistory).where(
                        ReminderHistory.medicine_id == med_id,
                        ReminderHistory.user_id == user_id
                    )
                )
                result = await session.execute(
                    delete(Medicine).where(
                        Medicine.id == med_id,
                        Medicine.user_id == user_id
                    )
                )
                await session.commit()
                return result.rowcount > 0
        else:
            if "medicines" in db_instance.in_memory_store:
                if med_id in db_instance.in_memory_store["medicines"]:
                    del db_instance.in_memory_store["medicines"][med_id]
                    return True
            return False

    @staticmethod
    async def log_reminder(reminder_doc: dict) -> dict:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                reminder_id = reminder_doc.get("_id") or reminder_doc.get("id")
                reminder = ReminderHistory(
                    id=reminder_id,
                    user_id=reminder_doc["user_id"],
                    medicine_id=reminder_doc["medicine_id"],
                    medicine_name=reminder_doc.get("medicine_name", "Prescription Pill"),
                    status=reminder_doc["status"],
                    timestamp=reminder_doc.get("timestamp")
                )
                session.add(reminder)
                await session.commit()
                await session.refresh(reminder)
                return reminder.to_dict()
        else:
            if "reminder_history" not in db_instance.in_memory_store:
                db_instance.in_memory_store["reminder_history"] = []
            db_instance.in_memory_store["reminder_history"].append(reminder_doc)
            return reminder_doc

    @staticmethod
    async def get_user_reminder_history(user_id: str) -> list:
        if db_instance.is_connected and db_instance.session_factory is not None:
            async with db_instance.session_factory() as session:
                result = await session.execute(
                    select(ReminderHistory)
                    .where(ReminderHistory.user_id == user_id)
                    .order_by(ReminderHistory.timestamp.desc())
                    .limit(100)
                )
                history = result.scalars().all()
                return [h.to_dict() for h in history]
        else:
            if "reminder_history" not in db_instance.in_memory_store:
                return []
            history = [r for r in db_instance.in_memory_store["reminder_history"] if r.get("user_id") == user_id]
            return sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)
