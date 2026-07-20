from fastapi import APIRouter, Depends, status
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
        id=med["_id"],
        user_id=med["user_id"],
        name=med["name"],
        dosage=med["dosage"],
        frequency=med["frequency"],
        times=med["times"],
        instructions=med["instructions"],
        is_active=med["is_active"],
        created_at=med["created_at"]
    )

@router.get("/", response_model=List[MedicineResponse])
async def list_medicines(current_user: UserResponse = Depends(get_current_user)):
    medicines = await MedicationRepository.get_user_medicines(current_user.id)
    return [
        MedicineResponse(
            id=m["_id"],
            user_id=m["user_id"],
            name=m["name"],
            dosage=m["dosage"],
            frequency=m["frequency"],
            times=m["times"],
            instructions=m["instructions"],
            is_active=m["is_active"],
            created_at=m["created_at"]
        ) for m in medicines
    ]

@router.post("/{med_id}/log", response_model=ReminderLogResponse)
async def log_reminder(med_id: str, payload: ReminderLogCreate, current_user: UserResponse = Depends(get_current_user)):
    log_doc = await MedicationService.log_reminder_status(med_id, payload, current_user.id)
    return ReminderLogResponse(
        id=log_doc["_id"],
        user_id=log_doc["user_id"],
        medicine_id=log_doc["medicine_id"],
        medicine_name=log_doc["medicine_name"],
        status=log_doc["status"],
        timestamp=log_doc["timestamp"]
    )

@router.get("/history", response_model=List[ReminderLogResponse])
async def get_reminder_history(current_user: UserResponse = Depends(get_current_user)):
    history = await MedicationRepository.get_user_reminder_history(current_user.id)
    return [
        ReminderLogResponse(
            id=h["_id"],
            user_id=h["user_id"],
            medicine_id=h["medicine_id"],
            medicine_name=h["medicine_name"],
            status=h["status"],
            timestamp=h["timestamp"]
        ) for h in history
    ]
