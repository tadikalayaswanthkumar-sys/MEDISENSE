from PIL import Image, ImageEnhance, ImageFilter
import io

def preprocess_image(image_bytes: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("L")  # Convert to Grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.8)  # Enhance Contrast for OCR
    return image
