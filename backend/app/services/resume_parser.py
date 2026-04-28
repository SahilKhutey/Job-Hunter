import pdfplumber
import docx
import io
import os
import asyncio

def _extract_text_from_pdf(file_content: bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def _extract_text_from_docx(file_content: bytes):
    doc = docx.Document(io.BytesIO(file_content))
    return "\n".join([p.text for p in doc.paragraphs])

async def extract_resume_text(filename: str, content: bytes):
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        return await asyncio.to_thread(_extract_text_from_pdf, content)
    elif ext in [".docx", ".doc"]:
        return await asyncio.to_thread(_extract_text_from_docx, content)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
