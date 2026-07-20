import pytest
from app.services.ocr.normalizer import BiomarkerNormalizer
from app.services.parser.report_parser import MedicalReportParser
from app.services.rag.rule_engine import AdvancedRuleEngine
from app.services.rag.vector_store import vector_store_instance
from app.services.rag.retriever import TargetedBiomarkerRetriever
from app.services.rag.rag_service import MedicalRAGService
from app.services.ai.gemini_service import GeminiService

def test_phase_1_ocr_biomarker_normalization():
    assert BiomarkerNormalizer.normalize_name("Hb") == "hemoglobin"
    assert BiomarkerNormalizer.normalize_name("Blood Sugar") == "glucose"
    assert BiomarkerNormalizer.normalize_name("Creat") == "creatinine"
    assert BiomarkerNormalizer.normalize_name("SGPT") == "alt"
    assert BiomarkerNormalizer.normalize_name("Vit D3") == "vitamin_d"

def test_phase_2_structured_medical_report_parser():
    ocr_text = """
    Patient Report: John Doe
    Hemoglobin (Hb) : 8.5 g/dL
    Fasting Blood Sugar : 210 mg/dL
    Serum Creatinine : 1.9 mg/dL
    """
    json_data = MedicalReportParser.parse_ocr_to_structured_json(ocr_text)
    
    assert "hemoglobin" in json_data
    assert json_data["hemoglobin"]["value"] == 8.5
    assert "glucose" in json_data
    assert json_data["glucose"]["value"] == 210.0
    assert "creatinine" in json_data
    assert json_data["creatinine"]["value"] == 1.9

def test_phase_3_rule_engine_classification_and_risk():
    json_data = {
        "hemoglobin": {"value": 8.2, "unit": "g/dL"},
        "glucose": {"value": 95.0, "unit": "mg/dL"}
    }
    normal, abnormal = AdvancedRuleEngine.classify_biomarkers(json_data, gender="Male")
    
    assert len(normal) == 1
    assert len(abnormal) == 1
    assert abnormal[0]["biomarker"] == "hemoglobin"
    assert abnormal[0]["status"] == "Critical Low"
    assert abnormal[0]["risk_level"] == "High"

def test_phase_7_8_targeted_per_biomarker_retrieval():
    abnormal = [{
        "biomarker": "creatinine",
        "name": "Serum Creatinine",
        "category": "Kidney Function",
        "value": 2.4,
        "unit": "mg/dL",
        "status": "Critical High"
    }]
    
    chunks = TargetedBiomarkerRetriever.retrieve_per_abnormal_biomarker(abnormal, top_k_per_biomarker=2)
    assert len(chunks) > 0
    assert chunks[0]["metadata"]["biomarker"] == "creatinine"

def test_phase_18_report_specificity_across_panels():
    # 1. CBC Anemia Report
    cbc_ocr = "Hemoglobin (Hb) - 8.2 g/dL"
    cbc_res = MedicalRAGService.process_rag_pipeline(cbc_ocr)

    # 2. Diabetes Report
    diabetes_ocr = "Fasting Blood Sugar: 220 mg/dL"
    diabetes_res = MedicalRAGService.process_rag_pipeline(diabetes_ocr)

    # 3. Kidney Report
    kidney_ocr = "Serum Creatinine : 2.5 mg/dL"
    kidney_res = MedicalRAGService.process_rag_pipeline(kidney_ocr)

    # 4. Liver Report
    liver_ocr = "ALT (SGPT) - 140 U/L"
    liver_res = MedicalRAGService.process_rag_pipeline(liver_ocr)

    # 5. Normal Report
    normal_ocr = "Fasting Glucose: 85 mg/dL, Hemoglobin: 14.5 g/dL"
    normal_res = MedicalRAGService.process_rag_pipeline(normal_ocr)

    # Assert DIFFERENT health scores across reports
    scores = {cbc_res["health_score"], diabetes_res["health_score"], kidney_res["health_score"], liver_res["health_score"], normal_res["health_score"]}
    assert len(scores) >= 4

    # Assert DIFFERENT retrieved documents
    cbc_doc = cbc_res["clinical_evidence"][0]["metadata"]["biomarker"]
    diabetes_doc = diabetes_res["clinical_evidence"][0]["metadata"]["biomarker"]
    kidney_doc = kidney_res["clinical_evidence"][0]["metadata"]["biomarker"]

    assert cbc_doc != diabetes_doc
    assert cbc_doc != kidney_doc
    assert diabetes_doc != kidney_doc
