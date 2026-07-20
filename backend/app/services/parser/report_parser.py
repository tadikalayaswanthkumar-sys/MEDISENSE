"""
MediSense AI - Structured Medical Report Parser
Converts OCR text into structured JSON for CBC, LFT, KFT, Thyroid, Lipid, HbA1c, Vit D, Vit B12.
"""

import re
from typing import Dict, Any
from app.services.ocr.normalizer import BiomarkerNormalizer

class MedicalReportParser:
    @staticmethod
    def parse_ocr_to_structured_json(ocr_text: str) -> Dict[str, Dict[str, Any]]:
        """
        Parses OCR text buffer into structured JSON representation of extracted biomarkers.
        Never passes unparsed raw text noise into the Vector Store.
        """
        if not ocr_text:
            return {}

        structured_results: Dict[str, Dict[str, Any]] = {}
        lines = ocr_text.split('\n')

        # Regular Expressions for value & unit extraction
        # Matches patterns like: "Fasting Glucose: 165.5 mg/dL", "Hb - 9.2 g/dL", "Serum Creatinine  1.8 mg/dL"
        pattern = re.compile(
            r'([a-zA-Z0-9\s\(\)\-\/\.]{2,40})'                      # Biomarker Name
            r'[:=\-\s]+'                                           # Separator
            r'([<>]?\s*\d+(?:\.\d+)?)'                             # Numeric Value
            r'\s*([a-zA-Z%/\^0-9\s\-]{1,15})?',                     # Unit
            re.IGNORECASE
        )

        for line in lines:
            line_str = line.strip()
            if not line_str or len(line_str) < 3:
                continue

            match = pattern.search(line_str)
            if match:
                raw_name = match.group(1).strip()
                val_str = match.group(2).strip().replace('<', '').replace('>', '').strip()
                raw_unit = match.group(3).strip() if match.group(3) else ""

                canonical_key = BiomarkerNormalizer.normalize_name(raw_name)
                if canonical_key:
                    try:
                        val = float(val_str)
                        structured_results[canonical_key] = {
                            "value": val,
                            "unit": raw_unit or MedicalReportParser._default_unit(canonical_key)
                        }
                    except ValueError:
                        continue

        return structured_results

    @staticmethod
    def _default_unit(key: str) -> str:
        """Returns standard medical unit for canonical biomarker."""
        units = {
            "glucose": "mg/dL",
            "hba1c": "%",
            "insulin": "uIU/mL",
            "cholesterol": "mg/dL",
            "hdl": "mg/dL",
            "ldl": "mg/dL",
            "triglycerides": "mg/dL",
            "hemoglobin": "g/dL",
            "wbc": "x10^3/uL",
            "rbc": "x10^6/uL",
            "platelets": "x10^3/uL",
            "hematocrit": "%",
            "mcv": "fL",
            "creatinine": "mg/dL",
            "bun": "mg/dL",
            "egfr": "mL/min/1.73m2",
            "uric_acid": "mg/dL",
            "alt": "U/L",
            "ast": "U/L",
            "bilirubin": "mg/dL",
            "albumin": "g/dL",
            "tsh": "uIU/mL",
            "vitamin_d": "ng/mL",
            "vitamin_b12": "pg/mL",
            "crp": "mg/L"
        }
        return units.get(key, "")
