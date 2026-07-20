import uuid
from datetime import datetime, timezone
from app.api.v1.medication.schemas import MedicineCreate, ReminderLogCreate
from app.api.v1.medication.repository import MedicationRepository

class MedicationService:
    @staticmethod
    async def add_medicine(payload: MedicineCreate, user_id: str) -> dict:
        med_doc = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "name": payload.name,
            "dosage": payload.dosage,
            "frequency": payload.frequency,
            "times": payload.times,
            "instructions": payload.instructions or "",
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        return await MedicationRepository.create_medicine(med_doc)

    @staticmethod
    async def log_reminder_status(med_id: str, payload: ReminderLogCreate, user_id: str) -> dict:
        medicines = await MedicationRepository.get_user_medicines(user_id)
        med_name = "Prescription Pill"
        for m in medicines:
            if m["_id"] == med_id:
                med_name = f"{m['name']} ({m['dosage']})"
                break
                
        log_doc = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "medicine_id": med_id,
            "medicine_name": med_name,
            "status": payload.status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return await MedicationRepository.log_reminder(log_doc)
