"""
MediSense AI - Redesigned Clinical Rule Engine & Dynamic Health Scoring
Classifies laboratory biomarkers into Normal, Borderline, Elevated, Critical High, Critical Low,
and calculates dynamic health scores based on clinical severity weights.
"""

from typing import Dict, List, Any, Tuple
from app.services.rag.knowledge_base import CLINICAL_KNOWLEDGE_BASE

class AdvancedRuleEngine:
    @staticmethod
    def classify_biomarkers(
        structured_json: Dict[str, Dict[str, Any]],
        age: int = 40,
        gender: str = "Male"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Classifies every extracted lab value against clinical reference ranges.
        Returns (normal_findings, abnormal_findings).
        """
        normal_findings = []
        abnormal_findings = []

        for key, item in structured_json.items():
            if isinstance(item, dict):
                val = item.get("val") if item.get("val") is not None else item.get("value")
                unit = item.get("unit", "")
            else:
                val = item
                unit = ""

            if val is None:
                continue

            kb_entry = CLINICAL_KNOWLEDGE_BASE.get(key.lower())
            if not kb_entry:
                continue

            status, risk_level, description = AdvancedRuleEngine._evaluate_clinical_bounds(
                key.lower(), val, kb_entry, gender
            )

            finding = {
                "key": key.lower(),
                "biomarker": key.lower(),
                "name": kb_entry["name"],
                "category": kb_entry["category"],
                "value": val,
                "unit": unit or kb_entry["unit"],
                "optimal_range": f"{kb_entry['optimal']['min']} - {kb_entry['optimal']['max']} {kb_entry['unit']}",
                "status": status,
                "risk_level": risk_level,
                "severity": "High" if risk_level == "High" or "Critical" in status or status in ["Elevated", "High"] else "Moderate",
                "description": description
            }

            if status == "Normal":
                normal_findings.append(finding)
            else:
                abnormal_findings.append(finding)

        return normal_findings, abnormal_findings

    @staticmethod
    def _evaluate_clinical_bounds(key: str, val: float, kb: dict, gender: str) -> tuple:
        """Evaluates lab value against clinical bounds."""
        opt_min = kb["optimal"]["min"]
        opt_max = kb["optimal"]["max"]

        if key == "hemoglobin" and gender.lower() == "female":
            opt_min = 12.0
            opt_max = 15.5

        if opt_min <= val <= opt_max:
            return "Normal", "Low", f"{kb['name']} is optimal at {val} {kb['unit']}."

        if val > opt_max:
            if key in ["glucose", "hba1c", "creatinine", "alt", "ast", "cholesterol", "triglycerides"] and val >= opt_max * 1.20:
                return "Critical High", "High", f"Critical High: {kb['name']} is {val} {kb['unit']} (Normal: {opt_min}-{opt_max})."
            if val <= opt_max * 1.15:
                return "Borderline Elevated", "Moderate", f"Borderline Elevated: {kb['name']} is {val} {kb['unit']} (Normal: {opt_min}-{opt_max})."
            return "Elevated", "Moderate", f"Elevated: {kb['name']} is {val} {kb['unit']} (Normal: {opt_min}-{opt_max})."

        if val < opt_min:
            if key in ["hemoglobin", "platelets", "hdl", "egfr", "vitamin_d"] and val <= opt_min * 0.70:
                return "Critical Low", "High", f"Critical Low: {kb['name']} is {val} {kb['unit']} (Normal: {opt_min}-{opt_max})."
            return "Low", "Moderate", f"Low: {kb['name']} is {val} {kb['unit']} (Normal: {opt_min}-{opt_max})."

        return "Abnormal", "Moderate", f"Abnormal: {kb['name']} is {val} {kb['unit']}."

    @staticmethod
    def construct_abnormal_vector_query(abnormal_findings: List[Dict[str, Any]], raw_text: str = "") -> str:
        """Constructs vector search query from abnormal findings."""
        if not abnormal_findings:
            return raw_text[:300] if raw_text else "optimal clinical lab values"

        query_parts = []
        for finding in abnormal_findings:
            query_parts.append(
                f"{finding['name']} {finding['value']} {finding['unit']} {finding['status']} {finding['category']}"
            )

        return " ".join(query_parts)

    @staticmethod
    def calculate_dynamic_health_score(abnormal_findings: List[Dict[str, Any]]) -> int:
        """Calculates dynamic health score (15-100)."""
        if not abnormal_findings:
            return 98

        base_score = 100
        clinical_weights = {
            "creatinine": 30,
            "glucose": 26,
            "hemoglobin": 25,
            "hba1c": 22,
            "alt": 20,
            "ast": 20,
            "cholesterol": 18,
            "triglycerides": 18,
            "tsh": 18,
            "vitamin_d": 12
        }

        for finding in abnormal_findings:
            key = finding.get("biomarker") or finding.get("key")
            risk = finding.get("risk_level", "Moderate")
            status = finding.get("status", "")

            weight = clinical_weights.get(key, 15)
            if risk == "High" or "Critical" in status or status in ["Elevated", "High"]:
                base_score -= weight
            else:
                base_score -= max(weight // 2, 6)

        return max(min(base_score, 100), 15)

# Backward Compatibility Alias
MedicalRuleEngine = AdvancedRuleEngine
