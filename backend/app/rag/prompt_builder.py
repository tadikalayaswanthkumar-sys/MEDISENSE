"""
MediSense AI - Prompt Builder
Formats Structured Findings + Retrieved Evidence + Patient Demographics for Gemini.
Removes raw OCR from LLM prompt to prevent noise and hallucinations.
"""

from typing import Dict, List, Any

class PromptBuilder:
    @staticmethod
    def build_grounded_prompt(
        abnormal_findings: List[Dict[str, Any]],
        normal_findings: List[Dict[str, Any]],
        retrieved_evidence: List[Dict[str, Any]],
        age: int = 40,
        gender: str = "Male"
    ) -> str:
        """
        Builds a strictly grounded prompt for Gemini passing ONLY structured findings and evidence.
        """
        # Format Abnormal Findings
        abnormal_text = ""
        for f in abnormal_findings:
            abnormal_text += (
                f"- {f.get('name', f.get('biomarker'))}: {f.get('value')} {f.get('unit')} "
                f"[{f.get('status', 'Abnormal')}] -> Range: {f.get('optimal_range', '')}. {f.get('description', '')}\n"
            )

        # Format Normal Findings Summary
        normal_text = ", ".join([f.get("name", f.get("biomarker")) for f in normal_findings])

        # Format Retrieved Medical Knowledge Chunks
        evidence_text = ""
        for idx, chunk in enumerate(retrieved_evidence):
            score = chunk.get("similarity_score", 0.0)
            meta = chunk.get("metadata", {})
            evidence_text += (
                f"--- EVIDENCE CHUNK #{idx+1} [Biomarker: {meta.get('biomarker', 'General')} | Score: {score:.4f}] ---\n"
                f"{chunk.get('text', '')}\n\n"
            )

        prompt = f"""
You are an expert Pathologist and Clinical Decision Support System for MediSense AI.

Analyze the patient laboratory findings below using ONLY the provided structured findings and retrieved clinical evidence.

--- PATIENT DEMOGRAPHICS ---
Age: {age} | Gender: {gender}

--- STRUCTURED ABNORMAL BIOMARKERS ---
{abnormal_text if abnormal_text else "All identified laboratory biomarkers are within optimal reference bounds."}

--- OPTIMAL NORMAL BIOMARKERS ---
{normal_text if normal_text else "None"}

--- RETRIEVED CLINICAL KNOWLEDGE EVIDENCE ---
{evidence_text if evidence_text else "Standard healthy baseline reference bounds apply."}

--- STRICT NON-HALLUCINATION INSTRUCTIONS ---
1. Never hallucinate lab values, diagnostic tests, or medical facts.
2. Base all explanations ONLY on the provided structured findings and retrieved evidence.
3. If evidence is missing for a finding, clearly state "Insufficient evidence available."
4. Explain each biomarker abnormality separately with specific dietary and lifestyle guidance.
5. Do NOT recommend prescription drugs. Provide non-pharmacological lifestyle, dietary, and doctor consultation advice ONLY.

--- REQUIRED JSON OUTPUT FORMAT ---
Respond ONLY with a valid JSON object matching this exact structure (no markdown wrapper):
{{
  "health_score": <Calculated score 0-100>,
  "risk_assessment": [
    {{
      "condition": "<Specific risk condition>",
      "risk_level": "<High | Moderate | Low>",
      "description": "<Clinical explanation grounded strictly in evidence>"
    }}
  ],
  "recommendations": [
    "<Biomarker-specific dietary or lifestyle recommendation grounded in evidence>"
  ],
  "summary": "<2-sentence clinical summary of overall report health>"
}}
"""
        return prompt.strip()
