import pdfplumber
from docx import Document
from fastapi import UploadFile
import tempfile


async def parse_resume(file: UploadFile):
    suffix = file.filename.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as temp:
        content = await file.read()
        temp.write(content)
        temp_path = temp.name

    if suffix == "pdf":
        return parse_pdf(temp_path)
    elif suffix == "docx":
        return parse_docx(temp_path)
    else:
        return "Unsupported file type"


def parse_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def parse_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
