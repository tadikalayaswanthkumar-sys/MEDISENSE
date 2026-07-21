import pytest
from app.services.rag.knowledge_base import CLINICAL_KNOWLEDGE_BASE
from app.services.rag.retriever import ClinicalRetriever
from app.services.rag.rag_service import MedicalRAGService
from app.services.ai.gemini_service import GeminiService

def test_clinical_knowledge_base_structure():
    assert "glucose" in CLINICAL_KNOWLEDGE_BASE
    assert "cholesterol" in CLINICAL_KNOWLEDGE_BASE
    assert "hemoglobin" in CLINICAL_KNOWLEDGE_BASE
    assert "creatinine" in CLINICAL_KNOWLEDGE_BASE
    assert "tsh" in CLINICAL_KNOWLEDGE_BASE

def test_diabetic_report_rag_analysis():
    biomarkers = {
        "glucose": {"val": 150.0, "unit": "mg/dL"},
        "hba1c": {"val": 7.2, "unit": "%"}
    }
    raw_text = "Fasting Glucose: 150 mg/dL, HbA1c: 7.2%"

    analysis = MedicalRAGService.process_rag_analysis(biomarkers, raw_text)
    
    assert analysis["health_score"] < 80
    assert any("Glucose" in r["condition"] or "Critical" in r["description"] or "Diabetes" in r["description"] for r in analysis["risk_assessment"])
    assert len(analysis["recommendations"]) > 0

def test_lipid_report_rag_analysis():
    biomarkers = {
        "cholesterol": {"val": 260.0, "unit": "mg/dL"},
        "triglycerides": {"val": 220.0, "unit": "mg/dL"}
    }
    raw_text = "Total Cholesterol: 260 mg/dL, Triglycerides: 220 mg/dL"

    analysis = MedicalRAGService.process_rag_analysis(biomarkers, raw_text)
    
    assert analysis["health_score"] < 85
    assert any("Cholesterol" in r["condition"] or "Hypercholesterolemia" in r["description"] for r in analysis["risk_assessment"])

def test_normal_report_rag_analysis():
    biomarkers = {
        "glucose": {"val": 85.0, "unit": "mg/dL"},
        "hemoglobin": {"val": 15.0, "unit": "g/dL"},
        "cholesterol": {"val": 170.0, "unit": "mg/dL"}
    }
    raw_text = "All values within normal range."

    analysis = MedicalRAGService.process_rag_analysis(biomarkers, raw_text)
    
    assert analysis["health_score"] >= 90
    assert analysis["risk_assessment"][0]["risk_level"] == "Low"

def test_different_reports_produce_different_data():
    diabetic_res = GeminiService.analyze_report({"glucose": {"val": 160.0, "unit": "mg/dL"}}, "Glucose 160")
    normal_res = GeminiService.analyze_report({"glucose": {"val": 85.0, "unit": "mg/dL"}}, "Glucose 85")
    lipid_res = GeminiService.analyze_report({"cholesterol": {"val": 250.0, "unit": "mg/dL"}}, "Cholesterol 250")

    # Verify distinct health scores and distinct risk conditions
    assert diabetic_res["health_score"] != normal_res["health_score"]
    assert diabetic_res["risk_assessment"][0]["condition"] != normal_res["risk_assessment"][0]["condition"]
    assert diabetic_res["risk_assessment"][0]["condition"] != lipid_res["risk_assessment"][0]["condition"]
