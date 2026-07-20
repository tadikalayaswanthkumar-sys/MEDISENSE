import pypdf
import logging

logger = logging.getLogger("uvicorn.error")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import io
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        extracted_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
        return "\n".join(extracted_text)
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""
