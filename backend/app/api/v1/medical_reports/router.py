from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from typing import List
from app.api.v1.medical_reports.schemas import ReportResponse
from app.api.v1.medical_reports.service import MedicalReportService
from app.api.v1.medical_reports.repository import MedicalReportRepository
from app.dependencies.current_user import get_current_user
from app.api.v1.auth.schemas import UserResponse

router = APIRouter(prefix="/reports", tags=["Medical Reports"])

@router.post("/upload", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def upload_medical_report(
    title: str = Form(""),
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided.")
        
    contents = await file.read()
    report_doc = await MedicalReportService.process_and_save_report(
        file_bytes=contents,
        filename=file.filename,
        title=title,
        user_id=current_user.id
    )
    
    return ReportResponse(
        id=report_doc["_id"],
        user_id=report_doc["user_id"],
        title=report_doc["title"],
        file_name=report_doc["file_name"],
        upload_date=report_doc["upload_date"],
        raw_text=report_doc["raw_text"],
        biomarkers=report_doc["biomarkers"],
        health_score=report_doc["health_score"],
        risk_assessment=report_doc["risk_assessment"],
        recommendations=report_doc["recommendations"],
        summary=report_doc["summary"]
    )

@router.get("/", response_model=List[ReportResponse])
async def list_reports(current_user: UserResponse = Depends(get_current_user)):
    reports = await MedicalReportRepository.get_user_reports(current_user.id)
    return [
        ReportResponse(
            id=r["_id"],
            user_id=r["user_id"],
            title=r["title"],
            file_name=r["file_name"],
            upload_date=r["upload_date"],
            raw_text=r["raw_text"],
            biomarkers=r["biomarkers"],
            health_score=r["health_score"],
            risk_assessment=r["risk_assessment"],
            recommendations=r["recommendations"],
            summary=r["summary"]
        ) for r in reports
    ]

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, current_user: UserResponse = Depends(get_current_user)):
    r = await MedicalReportRepository.get_report_by_id(report_id, current_user.id)
    if not r:
        raise HTTPException(status_code=404, detail="Medical report not found.")
    return ReportResponse(
        id=r["_id"],
        user_id=r["user_id"],
        title=r["title"],
        file_name=r["file_name"],
        upload_date=r["upload_date"],
        raw_text=r["raw_text"],
        biomarkers=r["biomarkers"],
        health_score=r["health_score"],
        risk_assessment=r["risk_assessment"],
        recommendations=r["recommendations"],
        summary=r["summary"]
    )
