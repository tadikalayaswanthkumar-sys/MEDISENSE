"""
MediSense AI - Biomarker Alias Normalizer
Normalizes raw OCR lab report terms into standardized clinical biomarker keys.
"""

import re
from typing import Optional

BIOMARKER_ALIAS_MAP = {
    # Glycemic & Metabolic
    "glucose": ["fasting blood sugar", "fbs", "blood sugar", "fasting glucose", "bgl", "glycemia", "plasma glucose"],
    "hba1c": ["glycated hemoglobin", "a1c", "hb a1c", "hemoglobin a1c", "glycohemoglobin"],
    "insulin": ["fasting insulin", "serum insulin", "immunoreactive insulin"],

    # Lipid Profile
    "cholesterol": ["total cholesterol", "s.cholesterol", "serum cholesterol", "chol"],
    "hdl": ["hdl cholesterol", "high density lipoprotein", "hdl-c", "good cholesterol"],
    "ldl": ["ldl cholesterol", "low density lipoprotein", "ldl-c", "bad cholesterol"],
    "triglycerides": ["tg", "trig", "serum triglycerides", "triglyceride"],

    # Complete Blood Count (CBC)
    "hemoglobin": ["hb", "hgb", "hemoglobin (hb)", "haemoglobin", "total hemoglobin"],
    "wbc": ["white blood cell", "white blood count", "total wbc", "tlc", "leukocytes"],
    "rbc": ["red blood cell", "red blood count", "total rbc", "erythrocytes"],
    "platelets": ["plt", "platelet count", "total platelets", "thrombocytes"],
    "hematocrit": ["hct", "packed cell volume", "pcv"],
    "mcv": ["mean corpuscular volume"],

    # Renal / Kidney Panel
    "creatinine": ["creat", "s.creatinine", "serum creatinine", "cr", "creatinine serum"],
    "bun": ["blood urea nitrogen", "urea nitrogen", "serum urea", "urea"],
    "egfr": ["estimated gfr", "gfr", "calculated egfr"],
    "uric_acid": ["s.uric acid", "serum uric acid", "urate"],

    # Liver Function Panel (LFT)
    "alt": ["sgpt", "alt (sgpt)", "alanine aminotransferase", "alanine transaminase"],
    "ast": ["sgot", "ast (sgot)", "aspartate aminotransferase", "aspartate transaminase"],
    "bilirubin": ["total bilirubin", "s.bilirubin", "serum bilirubin", "t.bilirubin"],
    "albumin": ["s.albumin", "serum albumin", "alb"],

    # Thyroid Panel
    "tsh": ["s.tsh", "serum tsh", "thyroid stimulating hormone", "thyrotropin"],

    # Vitamins & Minerals
    "vitamin_d": ["vit d", "vitamin d3", "25-oh vit d", "25-hydroxyvitamin d", "calcidiol"],
    "vitamin_b12": ["vit b12", "b12", "cobalamin", "cyanocobalamin"],

    # Inflammatory
    "crp": ["c-reactive protein", "hs-crp", "high sensitivity crp"]
}

class BiomarkerNormalizer:
    @staticmethod
    def normalize_name(raw_name: str) -> Optional[str]:
        """
        Normalizes any OCR extracted raw biomarker string into a canonical biomarker key.
        Returns None if not recognized.
        """
        if not raw_name:
            return None

        cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_name.lower()).strip()
        cleaned_words = cleaned.split()

        # Direct exact match check
        for canonical_key, aliases in BIOMARKER_ALIAS_MAP.items():
            if cleaned == canonical_key:
                return canonical_key
            for alias in aliases:
                if alias == cleaned:
                    return canonical_key

        # Substring / word boundary matching
        for canonical_key, aliases in BIOMARKER_ALIAS_MAP.items():
            for alias in aliases:
                if len(alias) >= 3 and alias in cleaned:
                    return canonical_key
            if canonical_key in cleaned:
                return canonical_key

        return None
