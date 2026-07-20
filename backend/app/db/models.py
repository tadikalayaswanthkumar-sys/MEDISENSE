from datetime import datetime, timezone
import uuid
from sqlalchemy import String, Boolean, Integer, JSON, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(100), default="User")
    avatar: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[str] = mapped_column(String(255), default=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "avatar": self.avatar,
            "is_active": self.is_active,
            "created_at": self.created_at
        }

class MedicalReport(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("users.id"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str] = mapped_column(String(500), nullable=True)
    file_path: Mapped[str] = mapped_column(Text, nullable=True)
    file_type: Mapped[str] = mapped_column(String(100), nullable=True)
    upload_date: Mapped[str] = mapped_column(String(255), default=lambda: datetime.now(timezone.utc).isoformat())
    raw_text: Mapped[str] = mapped_column(Text, nullable=True)
    health_score: Mapped[int] = mapped_column(Integer, default=90)
    biomarkers: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_assessment: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)
    summary: Mapped[str] = mapped_column(Text, nullable=True)

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "file_name": self.file_name or self.title,
            "file_path": self.file_path or "",
            "file_type": self.file_type or "text/plain",
            "upload_date": self.upload_date,
            "raw_text": self.raw_text or "",
            "health_score": self.health_score,
            "biomarkers": self.biomarkers or {},
            "risk_assessment": self.risk_assessment or [],
            "recommendations": self.recommendations or [],
            "summary": self.summary or ""
        }

class HealthRecord(Base):
    __tablename__ = "health_records"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("users.id"), index=True, nullable=False)
    report_id: Mapped[str] = mapped_column(String(255), ForeignKey("reports.id"), nullable=True)
    health_score: Mapped[int] = mapped_column(Integer, default=90)
    risk_assessment: Mapped[list] = mapped_column(JSON, default=list)
    biomarkers: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(String(255), default=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "id": self.id,
            "user_id": self.user_id,
            "report_id": self.report_id,
            "health_score": self.health_score,
            "risk_assessment": self.risk_assessment or [],
            "biomarkers": self.biomarkers or {},
            "created_at": self.created_at
        }

class Medicine(Base):
    __tablename__ = "medicines"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("users.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dosage: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency: Mapped[str] = mapped_column(String(255), nullable=False)
    times: Mapped[list] = mapped_column(JSON, default=list)
    instructions: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[str] = mapped_column(String(255), default=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "times": self.times or [],
            "instructions": self.instructions or "",
            "is_active": self.is_active,
            "created_at": self.created_at
        }

class ReminderHistory(Base):
    __tablename__ = "reminder_history"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("users.id"), index=True, nullable=False)
    medicine_id: Mapped[str] = mapped_column(String(255), nullable=False)
    medicine_name: Mapped[str] = mapped_column(String(255), nullable=True, default="Prescription Pill")
    status: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[str] = mapped_column(String(255), default=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "_id": self.id,
            "id": self.id,
            "user_id": self.user_id,
            "medicine_id": self.medicine_id,
            "medicine_name": self.medicine_name or "Prescription Pill",
            "status": self.status,
            "timestamp": self.timestamp
        }
