import pytest
from app.rag.embeddings import embedding_service
from app.rag.chunker import DocumentChunker
from app.rag.vector_db import vector_db
from app.rag.retriever import MedicalRetriever
from app.rag.prompt_builder import PromptBuilder
from app.rag.rag_service import ProductionRAGService
from app.services.ai.gemini_service import GeminiService

def test_embedding_service_batch_and_encoding():
    emb1 = embedding_service.encode_text("Hemoglobin level is low.")
    emb2 = embedding_service.encode_text("Blood glucose level is high.")
    
    assert len(emb1) == 384
    assert len(emb2) == 384
    assert emb1 != emb2

def test_document_chunker_word_based_with_metadata():
    chunks = DocumentChunker.chunk_markdown_file("app/rag/knowledge/cbc/hemoglobin.md")
    assert len(chunks) > 0
    assert "biomarker" in chunks[0]["metadata"]
    assert chunks[0]["metadata"]["biomarker"] == "hemoglobin"
    assert chunks[0]["metadata"]["category"] == "cbc"

def test_targeted_retriever_per_biomarker_metadata_filtering():
    abnormal = [
        {"biomarker": "creatinine", "name": "Serum Creatinine", "value": 2.2, "unit": "mg/dL", "status": "Critical High"}
    ]
    chunks = MedicalRetriever.retrieve_medical_evidence(abnormal, top_k_per_biomarker=3)
    assert len(chunks) > 0
    assert chunks[0]["metadata"]["biomarker"] == "creatinine"
    assert chunks[0]["metadata"]["category"] == "kidney"

def test_prompt_builder_without_raw_ocr():
    prompt = PromptBuilder.build_grounded_prompt(
        abnormal_findings=[{"name": "Fasting Glucose", "value": 210, "unit": "mg/dL", "status": "Critical High"}],
        normal_findings=[],
        retrieved_evidence=[{"text": "Sample clinical evidence", "similarity_score": 0.85, "metadata": {"biomarker": "glucose"}}]
    )
    assert "PATIENT DEMOGRAPHICS" in prompt
    assert "Fasting Glucose" in prompt
    assert "STRICT NON-HALLUCINATION INSTRUCTIONS" in prompt

def test_report_specificity_across_five_distinct_reports():
    # 1. Low Hemoglobin Report
    hemo_res = GeminiService.analyze_report({}, "Hemoglobin: 8.2 g/dL")

    # 2. High Glucose Report
    glucose_res = GeminiService.analyze_report({}, "Fasting Blood Sugar: 215 mg/dL")

    # 3. High Creatinine Report
    creat_res = GeminiService.analyze_report({}, "Serum Creatinine: 2.2 mg/dL")

    # 4. High ALT Report
    alt_res = GeminiService.analyze_report({}, "ALT (SGPT): 140 U/L")

    # 5. Healthy Report
    healthy_res = GeminiService.analyze_report({}, "Fasting Glucose: 85 mg/dL, Hemoglobin: 14.5 g/dL")

    # Assert distinct health scores
    scores = {hemo_res["health_score"], glucose_res["health_score"], creat_res["health_score"], alt_res["health_score"], healthy_res["health_score"]}
    assert len(scores) >= 4

    # Assert distinct evidence retrieved
    hemo_bm = hemo_res["clinical_evidence"][0]["metadata"]["biomarker"]
    glucose_bm = glucose_res["clinical_evidence"][0]["metadata"]["biomarker"]
    creat_bm = creat_res["clinical_evidence"][0]["metadata"]["biomarker"]

    assert hemo_bm == "hemoglobin"
    assert glucose_bm == "glucose"
    assert creat_bm == "creatinine"
    assert hemo_bm != glucose_bm
    assert glucose_bm != creat_bm
