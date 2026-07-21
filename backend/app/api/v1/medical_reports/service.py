import uuid
from datetime import datetime, timezone
from app.services.ocr.ocr_service import OCRService
from app.services.ai.gemini_service import GeminiService
from app.api.v1.medical_reports.repository import MedicalReportRepository

class MedicalReportService:
    @staticmethod
    async def process_and_save_report(file_bytes: bytes, filename: str, title: str, user_id: str) -> dict:
        # Step 1: Run OCR service text & biomarker extraction using title, filename & bytes
        ocr_result = OCRService.process_file_content(file_bytes, filename, title or "")
        
        # Step 2: Run RAG-augmented AI disease risk prediction & health scoring
        ai_result = GeminiService.analyze_report(ocr_result["biomarkers"], ocr_result["raw_text"])
        
        # Step 3: Construct Document & save to Database
        report_doc = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": title or filename,
            "file_name": filename,
            "upload_date": datetime.now(timezone.utc).isoformat(),
            "raw_text": ocr_result["raw_text"],
            "biomarkers": ocr_result["biomarkers"],
            "health_score": ai_result["health_score"],
            "risk_assessment": ai_result["risk_assessment"],
            "recommendations": ai_result["recommendations"],
            "summary": ai_result["summary"]
        }
        
        return await MedicalReportRepository.create_report(report_doc)
