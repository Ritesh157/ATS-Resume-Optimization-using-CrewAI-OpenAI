import io # helps treat raw bytes like a file
from typing import Tuple
from pypdf import PdfReader
from docx import Document

''''
This function gets PDF file data and gives back the extracted text.
Creates an empty list to collect text from each page.
Go through each page in the PDF.
Try to get text from the page. If nothing is found, use an empty string.
Store the text from this page.
Combine all page texts into one string separated by new lines.
'''
def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        parts.append(txt)
    return "\n".join(parts)

'''
This function extracts text from a .docx document.
Convert bytes into a fake file. Open it using Document.
Read all paragraphs and collect their text.
Join all paragraphs into one text
'''
def extract_text_from_docx(file_bytes: bytes) -> str:
    f = io.BytesIO(file_bytes)
    doc = Document(f)
    parts = []
    for p in doc.paragraphs:
        parts.append(p.text)
    return "\n".join(parts)

'''
This function:
    1) Looks at the file name → identifies file type
    2) Extracts text using the correct method.

Makes file name lowercase to avoid case issues.

'''
def detect_and_extract(filename: str, file_bytes: bytes) -> Tuple[str, str]:
    """Return (ext, text). ext in {pdf, docx, txt}."""
    low = filename.lower()
    if low.endswith(".pdf"):
        return "pdf", extract_text_from_pdf(file_bytes)
    if low.endswith(".docx"):
        return "docx", extract_text_from_docx(file_bytes)
    # Basic text fallback
    # Try to turn the bytes into simple text
    # If everything fails means file is unknown (binary), return empty text.
    try:
        return "txt", file_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return "bin", ""



