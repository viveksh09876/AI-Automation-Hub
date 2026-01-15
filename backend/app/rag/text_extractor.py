from pathlib import Path
import fitz


def extract_text_from_pdf(file_path: Path) -> str:
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text
