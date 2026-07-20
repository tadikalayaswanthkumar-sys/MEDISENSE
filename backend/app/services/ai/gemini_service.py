import json
import logging
import google.generativeai as genai
from app.config.settings import settings
from app.services.ai.prompt_builder import PromptBuilder

logger = logging.getLogger("uvicorn.error")

class GeminiService:
    @staticmethod
    def analyze_report(biomarkers: dict, raw_text: str) -> dict:
        if settings.GEMINI_API_KEY:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = PromptBuilder.build_medical_analysis_prompt(biomarkers, raw_text)
                response = model.generate_content(prompt)
                
                clean_json_str = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_json_str)
            except Exception as e:
                logger.warning(f"Gemini API call failed: {e}. Falling back to medical rules engine.")

        # Fallback Medical Rule Engine Analysis
        return GeminiService._rule_based_fallback_analysis(biomarkers)

    @staticmethod
    def _rule_based_fallback_analysis(biomarkers: dict) -> dict:
        score = 92
        risks = []
        recommendations = [
            "Maintain adequate daily hydration (2-3 Liters of water).",
            "Engage in 30 minutes of moderate cardiovascular activity daily.",
            "Schedule an annual routine physical exam."
        ]

        if "glucose" in biomarkers:
            g_val = biomarkers["glucose"]["val"]
            if g_val >= 126:
                score -= 15
                risks.append({
                    "condition": "Hyperglycemia / Diabetes Risk",
                    "risk_level": "High",
                    "description": f"Fasting glucose level is elevated at {g_val} mg/dL (Normal: < 100 mg/dL)."
                })
                recommendations.append("Reduce refined sugar intake and monitor carbohydrate consumption.")
            elif g_val >= 100:
                score -= 8
                risks.append({
                    "condition": "Prediabetes Risk",
                    "risk_level": "Moderate",
                    "description": f"Fasting blood glucose is slightly elevated at {g_val} mg/dL."
                })

        if "cholesterol" in biomarkers:
            c_val = biomarkers["cholesterol"]["val"]
            if c_val >= 240:
                score -= 12
                risks.append({
                    "condition": "Hypercholesterolemia",
                    "risk_level": "High",
                    "description": f"Total cholesterol is high at {c_val} mg/dL (Desirable: < 200 mg/dL)."
                })
                recommendations.append("Adopt a heart-healthy diet rich in soluble fiber and low in saturated fats.")
            elif c_val >= 200:
                score -= 6
                risks.append({
                    "condition": "Borderline High Cholesterol",
                    "risk_level": "Moderate",
                    "description": f"Total cholesterol level is borderline at {c_val} mg/dL."
                })

        if "hemoglobin" in biomarkers:
            hb_val = biomarkers["hemoglobin"]["val"]
            if hb_val < 12.0:
                score -= 10
                risks.append({
                    "condition": "Anemia Risk",
                    "risk_level": "Moderate",
                    "description": f"Hemoglobin level is low at {hb_val} g/dL."
                })
                recommendations.append("Increase iron-rich foods in your diet (spinach, legumes, lean protein).")

        if not risks:
            risks.append({
                "condition": "Cardiovascular & Metabolic Health",
                "risk_level": "Low",
                "description": "All identified lab values remain within optimal clinical reference ranges."
            })

        summary = f"Your lab report indicates an overall health score of {score}/100. " + (
            "No urgent disease risks were identified." if score > 85 else f"Key parameters require attention: {risks[0]['condition']}."
        )

        return {
            "health_score": max(min(score, 100), 20),
            "risk_assessment": risks,
            "recommendations": recommendations,
            "summary": summary
        }
