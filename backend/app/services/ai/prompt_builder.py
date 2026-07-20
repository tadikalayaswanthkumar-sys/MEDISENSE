class PromptBuilder:
    @staticmethod
    def build_medical_analysis_prompt(biomarkers: dict, raw_text: str) -> str:
        prompt = f"""
You are MediSense AI, an expert medical analysis engine.
Analyze the following patient lab report data and biomarkers:

Extracted Biomarkers:
{biomarkers}

Report Content Snippet:
{raw_text}

Provide your evaluation in strict JSON format with the following structure:
{{
  "health_score": <number between 0 and 100 representing overall health status>,
  "risk_assessment": [
    {{
      "condition": "<name of disease/condition, e.g. Type 2 Diabetes, Hyperlipidemia, Anemia>",
      "risk_level": "<Low | Moderate | High>",
      "description": "<brief 1-2 sentence medical explanation of why this risk was flagged>"
    }}
  ],
  "recommendations": [
    "<actionable dietary, exercise, or lifestyle recommendation>"
  ],
  "summary": "<2-3 sentence easy-to-understand summary of the patient report for a non-medical user>"
}}
Return ONLY valid JSON.
"""
        return prompt
