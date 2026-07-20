from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ReportResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_name: str
    upload_date: str
    raw_text: str
    biomarkers: Dict[str, Any]
    health_score: int
    risk_assessment: List[Dict[str, Any]]
    recommendations: List[str]
    summary: str
