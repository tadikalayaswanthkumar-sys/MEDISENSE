"""
MediSense AI - Production-Grade RAG Pipeline Coordinator & Audit Logger
Executes complete 18-phase Vector-RAG architecture:
OCR Audit -> Medical Report Parser -> Rule Engine -> Per-Biomarker Vector Retriever -> Grounded Gemini Generation.
"""

import logging
from typing import Dict, List, Any
from app.services.parser.report_parser import MedicalReportParser
from app.services.rag.rule_engine import AdvancedRuleEngine
from app.services.rag.retriever import TargetedBiomarkerRetriever

logger = logging.getLogger("uvicorn.error")

class MedicalRAGService:
    @staticmethod
    def process_rag_pipeline(ocr_text: str, age: int = 40, gender: str = "Male") -> Dict[str, Any]:
        """
        Executes end-to-end production RAG pipeline:
        1. Parses raw OCR text into structured JSON.
        2. Evaluates lab values via Clinical Rule Engine (Normal vs Abnormal findings).
        3. Executes per-biomarker targeted vector retrieval with metadata filtering.
        4. Calculates dynamic report-specific health score & grounded recommendations.
        """
        # Phase 1 & 2: Structured Medical Report Parsing
        structured_json = MedicalReportParser.parse_ocr_to_structured_json(ocr_text)
        logger.info(f"[RAG AUDIT LOG] Parsed {len(structured_json)} structured biomarkers from OCR text.")

        # Phase 3: Rule Engine Pre-Classification
        normal_findings, abnormal_findings = AdvancedRuleEngine.classify_biomarkers(
            structured_json, age=age, gender=gender
        )
        logger.info(f"[RAG AUDIT LOG] Rule Engine: {len(normal_findings)} Normal, {len(abnormal_findings)} Abnormal Findings.")

        # Phase 7 & 8: Per-Biomarker Targeted Retrieval & Metadata Filtering
        retrieved_evidence = TargetedBiomarkerRetriever.retrieve_per_abnormal_biomarker(
            abnormal_findings, top_k_per_biomarker=2, min_score=0.20
        )
        logger.info(f"[RAG AUDIT LOG] Retrieved {len(retrieved_evidence)} deduplicated clinical knowledge chunks.")

        # Phase 13: Dynamic Health Score Calculation
        health_score = AdvancedRuleEngine.calculate_dynamic_health_score(abnormal_findings)

        # Build Risk Assessment & Grounded Evidence Recommendations
        risk_assessment = []
        recommendations = []
        retrieval_scores = []

        for chunk in retrieved_evidence:
            score = chunk.get("similarity_score", 0.0)
            meta = chunk.get("metadata", {})
            retrieval_scores.append({
                "biomarker": meta.get("biomarker"),
                "similarity_score": score,
                "source_file": meta.get("source_file")
            })

            text_snippet = chunk.get("text", "")
            if "Diet:" in text_snippet:
                diet_part = text_snippet.split("Diet:")[-1].split("\n")[0].strip()
                if diet_part and len(diet_part) > 10:
                    recommendations.append(diet_part)
            if "Exercise:" in text_snippet:
                ex_part = text_snippet.split("Exercise:")[-1].split("\n")[0].strip()
                if ex_part and len(ex_part) > 10:
                    recommendations.append(ex_part)

        for finding in abnormal_findings:
            risk_assessment.append({
                "condition": f"{finding['name']} {finding['status']}",
                "risk_level": finding["risk_level"],
                "description": finding["description"]
            })

        if not risk_assessment:
            risk_assessment.append({
                "condition": "Optimal Clinical Health Status",
                "risk_level": "Low",
                "description": "All identified laboratory biomarkers remain within optimal reference bounds."
            })

        if not recommendations:
            recommendations = [
                "Maintain adequate daily fluid hydration (2 - 3 Liters of water).",
                "Engage in 150 minutes of moderate aerobic physical activity weekly.",
                "Schedule an annual routine wellness check with your primary physician."
            ]

        # Deduplicate recommendations
        recommendations = list(dict.fromkeys(recommendations))

        if abnormal_findings:
            summary = f"Lab analysis indicates an overall health score of {health_score}/100 with {len(abnormal_findings)} abnormal biomarkers requiring attention."
        else:
            summary = f"Lab analysis indicates an optimal health score of {health_score}/100. All tested biomarkers are within normal reference ranges."

        confidence_score = 0.95 if abnormal_findings else 0.99

        return {
            "health_score": health_score,
            "risk_assessment": risk_assessment,
            "recommendations": recommendations,
            "summary": summary,
            "abnormal_findings": abnormal_findings,
            "normal_findings": normal_findings,
            "clinical_evidence": retrieved_evidence,
            "retrieval_scores": retrieval_scores,
            "confidence_score": confidence_score
        }

    # Backward Compatibility Aliases
    process_rag_analysis = staticmethod(lambda b, t: MedicalRAGService.process_rag_pipeline(t if isinstance(t, str) else str(b)))

    @staticmethod
    def build_grounded_gemini_prompt(rag_result: Dict[str, Any]) -> str:
        """
        Phase 11 & 12: Builds strictly grounded prompt passing ONLY structured findings and evidence.
        Enforces strict non-hallucination rules (forbids diagnosing, inventing values, recommending medicines).
        """
        abnormal_str = ""
        for f in rag_result.get("abnormal_findings", []):
            abnormal_str += f"- {f['name']}: {f['value']} {f['unit']} ({f['status']}) -> {f['description']}\n"

        evidence_str = ""
        for idx, doc in enumerate(rag_result.get("clinical_evidence", [])):
            evidence_str += f"[Evidence Chunk #{idx+1} | Score: {doc.get('similarity_score', 0)}]: {doc.get('text')}\n\n"

        prompt = f"""
You are an expert Clinical Decision Support AI for MediSense AI.

Analyze the patient report using ONLY the provided structured findings and retrieved clinical evidence.

--- STRUCTURED ABNORMAL BIOMARKERS ---
{abnormal_str if abnormal_str else "All biomarkers are within optimal reference ranges."}

--- RETRIEVED CLINICAL KNOWLEDGE EVIDENCE ---
{evidence_str if evidence_str else "Standard healthy baseline reference ranges apply."}

--- STRICT NON-HALLUCINATION RULES ---
1. Do NOT invent lab values, units, or test results not present in the input.
2. Do NOT diagnose medical conditions definitively. Explain findings as lab risk indicators.
3. Do NOT recommend prescription medicines. Provide lifestyle, dietary, and physician consultation guidance ONLY.
4. If evidence is insufficient for a finding, state "Insufficient evidence available."

--- OUTPUT FORMAT ---
Respond ONLY with a valid JSON object matching this exact schema (no markdown block wrapper):
{{
  "health_score": {rag_result['health_score']},
  "risk_assessment": [
    {{
      "condition": "<Risk condition indicator>",
      "risk_level": "<High | Moderate | Low>",
      "description": "<Clinical explanation grounded in lab values>"
    }}
  ],
  "recommendations": [
    "<Actionable dietary/lifestyle recommendation grounded in evidence>"
  ],
  "summary": "<2-sentence clinical summary of overall report health>"
}}
"""
        return prompt.strip()
