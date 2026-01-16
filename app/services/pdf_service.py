import logging
from io import BytesIO
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts text from a PDF file content (bytes) using pdfminer.six.
    Includes LAParams for better handling of multi-column layouts.
    """
    try:
        laparams = LAParams()
        text = extract_text(BytesIO(file_content), laparams=laparams)
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting PDF: {e}")
        return ""