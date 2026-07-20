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
        id=str(report_doc.get("_id") or report_doc.get("id")),
        user_id=str(report_doc["user_id"]),
        title=str(report_doc["title"]),
        file_name=str(report_doc.get("file_name") or report_doc.get("title") or file.filename),
        upload_date=str(report_doc["upload_date"]),
        raw_text=str(report_doc.get("raw_text", "")),
        biomarkers=report_doc.get("biomarkers", {}),
        health_score=int(report_doc.get("health_score", 90)),
        risk_assessment=report_doc.get("risk_assessment", []),
        recommendations=report_doc.get("recommendations", []),
        summary=str(report_doc.get("summary", ""))
    )

@router.get("/", response_model=List[ReportResponse])
async def list_reports(current_user: UserResponse = Depends(get_current_user)):
    reports = await MedicalReportRepository.get_user_reports(current_user.id)
    return [
        ReportResponse(
            id=str(r.get("_id") or r.get("id")),
            user_id=str(r["user_id"]),
            title=str(r["title"]),
            file_name=str(r.get("file_name") or r.get("title")),
            upload_date=str(r["upload_date"]),
            raw_text=str(r.get("raw_text", "")),
            biomarkers=r.get("biomarkers", {}),
            health_score=int(r.get("health_score", 90)),
            risk_assessment=r.get("risk_assessment", []),
            recommendations=r.get("recommendations", []),
            summary=str(r.get("summary", ""))
        ) for r in reports
    ]

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, current_user: UserResponse = Depends(get_current_user)):
    r = await MedicalReportRepository.get_report_by_id(report_id, current_user.id)
    if not r:
        raise HTTPException(status_code=404, detail="Medical report not found.")
    return ReportResponse(
        id=str(r.get("_id") or r.get("id")),
        user_id=str(r["user_id"]),
        title=str(r["title"]),
        file_name=str(r.get("file_name") or r.get("title")),
        upload_date=str(r["upload_date"]),
        raw_text=str(r.get("raw_text", "")),
        biomarkers=r.get("biomarkers", {}),
        health_score=int(r.get("health_score", 90)),
        risk_assessment=r.get("risk_assessment", []),
        recommendations=r.get("recommendations", []),
        summary=str(r.get("summary", ""))
    )
