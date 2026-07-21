"""
MediSense AI - Grounded Gemini Service
Calls Gemini 1.5 with strictly grounded prompts constructed by PromptBuilder.
"""

import json
import logging
import google.generativeai as genai
from app.config.settings import settings
from app.rag.rag_service import ProductionRAGService
from app.rag.prompt_builder import PromptBuilder

logger = logging.getLogger("uvicorn.error")

class GeminiService:
    @staticmethod
    def analyze_report(biomarkers: dict, raw_text: str) -> dict:
        """
        Executes production RAG architecture and calls Gemini with grounded prompts.
        """
        ocr_input = raw_text if raw_text else str(biomarkers)
        rag_result = ProductionRAGService.process_report_pipeline(ocr_input)

        if settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')

                prompt = PromptBuilder.build_grounded_prompt(
                    abnormal_findings=rag_result.get("abnormal_findings", []),
                    normal_findings=rag_result.get("normal_findings", []),
                    retrieved_evidence=rag_result.get("clinical_evidence", [])
                )

                response = model.generate_content(prompt)
                clean_json_str = response.text.replace("```json", "").replace("```", "").strip()
                ai_dict = json.loads(clean_json_str)

                rag_result["health_score"] = int(ai_dict.get("health_score", rag_result["health_score"]))
                rag_result["risk_assessment"] = ai_dict.get("risk_assessment", rag_result["risk_assessment"])
                rag_result["recommendations"] = ai_dict.get("recommendations", rag_result["recommendations"])
                rag_result["summary"] = ai_dict.get("summary", rag_result["summary"])

                return rag_result
            except Exception as e:
                logger.warning(f"[GEMINI RAG] Gemini LLM warning ({e}). Returning grounded RAG pipeline output.")

        return rag_result
