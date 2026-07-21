from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.v1.medication.schemas import MedicineCreate, MedicineResponse, ReminderLogCreate, ReminderLogResponse
from app.api.v1.medication.service import MedicationService
from app.api.v1.medication.repository import MedicationRepository
from app.dependencies.current_user import get_current_user
from app.api.v1.auth.schemas import UserResponse

router = APIRouter(prefix="/medication", tags=["Medication Tracker"])

@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
async def create_medicine(payload: MedicineCreate, current_user: UserResponse = Depends(get_current_user)):
    med = await MedicationService.add_medicine(payload, current_user.id)
    return MedicineResponse(
        id=str(med.get("_id") or med.get("id")),
        user_id=str(med["user_id"]),
        name=str(med["name"]),
        dosage=str(med["dosage"]),
        frequency=str(med["frequency"]),
        times=med.get("times", []),
        instructions=str(med.get("instructions", "")),
        is_active=bool(med.get("is_active", True)),
        created_at=str(med.get("created_at", ""))
    )

@router.get("/", response_model=List[MedicineResponse])
async def list_medicines(current_user: UserResponse = Depends(get_current_user)):
    medicines = await MedicationRepository.get_user_medicines(current_user.id)
    return [
        MedicineResponse(
            id=str(m.get("_id") or m.get("id")),
            user_id=str(m["user_id"]),
            name=str(m["name"]),
            dosage=str(m["dosage"]),
            frequency=str(m["frequency"]),
            times=m.get("times", []),
            instructions=str(m.get("instructions", "")),
            is_active=bool(m.get("is_active", True)),
            created_at=str(m.get("created_at", ""))
        ) for m in medicines
    ]

@router.delete("/{med_id}", status_code=status.HTTP_200_OK)
async def delete_medicine(med_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Deletes a prescription reminder."""
    deleted = await MedicationRepository.delete_medicine_by_id(med_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Medication reminder not found or unauthorized.")
    return {"message": "Prescription reminder deleted successfully", "id": med_id}

@router.post("/{med_id}/log", response_model=ReminderLogResponse)
async def log_reminder(med_id: str, payload: ReminderLogCreate, current_user: UserResponse = Depends(get_current_user)):
    log_doc = await MedicationService.log_reminder_status(med_id, payload, current_user.id)
    return ReminderLogResponse(
        id=str(log_doc.get("_id") or log_doc.get("id")),
        user_id=str(log_doc["user_id"]),
        medicine_id=str(log_doc["medicine_id"]),
        medicine_name=str(log_doc.get("medicine_name", "Prescription Pill")),
        status=str(log_doc["status"]),
        timestamp=str(log_doc["timestamp"])
    )

@router.get("/history", response_model=List[ReminderLogResponse])
async def get_reminder_history(current_user: UserResponse = Depends(get_current_user)):
    history = await MedicationRepository.get_user_reminder_history(current_user.id)
    return [
        ReminderLogResponse(
            id=str(h.get("_id") or h.get("id")),
            user_id=str(h["user_id"]),
            medicine_id=str(h["medicine_id"]),
            medicine_name=str(h.get("medicine_name", "Prescription Pill")),
            status=str(h["status"]),
            timestamp=str(h["timestamp"])
        ) for h in history
    ]
