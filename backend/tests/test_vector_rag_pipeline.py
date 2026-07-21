import pytest
from app.services.rag.chunker import DocumentChunker
from app.services.rag.vector_store import VectorStore
from app.services.rag.rule_engine import MedicalRuleEngine
from app.services.rag.retriever import ClinicalVectorRetriever
from app.services.rag.rag_service import MedicalRAGService
from app.services.ai.gemini_service import GeminiService

def test_document_chunking_tokens_and_overlap():
    sample_text = "Biomarker Glucose: 165 mg/dL. " * 50
    chunks = DocumentChunker.chunk_text(sample_text, chunk_size=300, overlap=50)
    
    assert len(chunks) > 1
    assert "id" in chunks[0]
    assert "token_estimate" in chunks[0]["metadata"]

def test_vector_store_embedding_and_similarity_search():
    vs = VectorStore()
    vs.initialize_and_index()
    
    results = vs.similarity_search("glucose elevated diabetes", top_k=3, min_score=0.20)
    assert len(results) > 0
    assert results[0]["similarity_score"] >= 0.20
    meta = results[0]["metadata"]
    assert "biomarker" in meta or "biomarker_key" in meta

def test_rule_engine_lab_value_pre_classification():
    biomarkers = {
        "glucose": {"val": 165.0, "unit": "mg/dL"},
        "hemoglobin": {"val": 14.5, "unit": "g/dL"}
    }
    normal, abnormal = MedicalRuleEngine.classify_biomarkers(biomarkers)
    
    assert len(normal) == 1
    assert len(abnormal) == 1
    assert abnormal[0]["key"] == "glucose"
    assert abnormal[0]["status"] == "Critical High"

def test_abnormal_vector_query_construction():
    _, abnormal = MedicalRuleEngine.classify_biomarkers({"creatinine": {"val": 2.4, "unit": "mg/dL"}})
    query = MedicalRuleEngine.construct_abnormal_vector_query(abnormal, "Raw report text")
    
    assert "Creatinine" in query or "creatinine" in query.lower()
    assert "2.4" in query

def test_clinical_vector_retriever_logging_and_scoring():
    query = "Serum Creatinine 2.4 mg/dL Critical High Kidney Function"
    results = ClinicalVectorRetriever.retrieve_medical_evidence(query, top_k=3, min_score=0.20)
    
    assert len(results) > 0
    assert "similarity_score" in results[0]

def test_full_vector_rag_pipeline_report_specificity():
    diabetic_res = GeminiService.analyze_report({"glucose": {"val": 175.0, "unit": "mg/dL"}}, "Glucose 175")
    kidney_res = GeminiService.analyze_report({"creatinine": {"val": 2.5, "unit": "mg/dL"}}, "Creatinine 2.5")
    normal_res = GeminiService.analyze_report({"glucose": {"val": 85.0, "unit": "mg/dL"}}, "Glucose 85")

    assert diabetic_res["health_score"] != kidney_res["health_score"]
    assert diabetic_res["health_score"] != normal_res["health_score"]
    assert diabetic_res["risk_assessment"][0]["condition"] != kidney_res["risk_assessment"][0]["condition"]
