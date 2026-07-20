from pydantic import BaseModel, Field
from typing import List, Optional

class MedicineCreate(BaseModel):
    name: str = Field(..., example="Atorvastatin")
    dosage: str = Field(..., example="10mg")
    frequency: str = Field("Once Daily", example="Once Daily")
    times: List[str] = Field(default_factory=lambda: ["08:00 AM"])
    instructions: Optional[str] = Field("", example="Take after breakfast")

class MedicineResponse(BaseModel):
    id: str
    user_id: str
    name: str
    dosage: str
    frequency: str
    times: List[str]
    instructions: str
    is_active: bool
    created_at: str

class ReminderLogCreate(BaseModel):
    status: str = Field(..., example="Taken")  # "Taken" or "Skipped"

class ReminderLogResponse(BaseModel):
    id: str
    user_id: str
    medicine_id: str
    medicine_name: str
    status: str
    timestamp: str
