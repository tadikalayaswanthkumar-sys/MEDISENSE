import re
from app.services.ocr.pdf_reader import extract_text_from_pdf

class OCRService:
    @staticmethod
    def extract_lab_values(text: str) -> dict:
        biomarkers = {}
        if not text:
            return biomarkers

        patterns = {
            "glucose": r"(?:glucose|fasting blood sugar|fbs)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(mg/dl|mmol/l)?",
            "cholesterol": r"(?:total cholesterol|cholesterol)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(mg/dl)?",
            "hdl": r"(?:hdl|hdl cholesterol)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(mg/dl)?",
            "ldl": r"(?:ldl|ldl cholesterol)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(mg/dl)?",
            "triglycerides": r"(?:triglycerides)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(mg/dl)?",
            "hemoglobin": r"(?:hemoglobin|hgb|hb)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(g/dl)?",
            "tsh": r"(?:tsh|thyroid stimulating hormone)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(uIU/ml|mIU/L)?",
            "wbc": r"(?:wbc|white blood cell count|leukocytes)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(x10\^3/uL|/uL)?",
            "platelets": r"(?:platelets|plt)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(x10\^3/uL|/uL)?",
            "hba1c": r"(?:hba1c|glycated hemoglobin)\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(%)?",
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                unit = match.group(2) if len(match.groups()) > 1 and match.group(2) else ""
                biomarkers[key] = {"val": value, "unit": unit}
                
        return biomarkers

    @staticmethod
    def process_file_content(file_bytes: bytes, filename: str) -> dict:
        filename_lower = filename.lower()
        text = ""
        
        if filename_lower.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        elif any(filename_lower.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff"]):
            # For image files, avoid binary string corruption
            text = f"Medical report image uploaded: {filename}"
        else:
            # Plain text files
            try:
                text = file_bytes.decode("utf-8", errors="ignore")
            except Exception:
                text = ""

        # Remove null bytes (\x00) which PostgreSQL strictly disallows in UTF-8 text fields
        clean_text = text.replace("\x00", "").replace("\u0000", "").strip() if text else ""
        if not clean_text:
            clean_text = f"Medical lab report uploaded: {filename}"

        # Extracted biomarkers map
        extracted_biomarkers = OCRService.extract_lab_values(clean_text)
        
        return {
            "raw_text": clean_text[:2000],
            "biomarkers": extracted_biomarkers
        }
