from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
import os

def generate_resume_pdf(data: dict, file_path: str):
    """
    Generates a professional, clean PDF resume from structured data.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    doc = SimpleDocTemplate(file_path, pagesize=LETTER, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor("#1e1b4b"), # Deep indigo
        spaceAfter=12
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor("#4f46e5"), # Violet
        spaceBefore=14,
        spaceAfter=8,
        borderPadding=(0, 0, 1, 0),
        borderWidth=0.5,
        borderColor=HexColor("#e5e7eb")
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    elements = []

    # Summary
    elements.append(Paragraph("Professional Summary", header_style))
    elements.append(Paragraph(data.get("summary", ""), body_style))
    elements.append(Spacer(1, 12))

    # Skills
    elements.append(Paragraph("Core Competencies", header_style))
    skills_text = ", ".join(data.get("skills", []))
    elements.append(Paragraph(skills_text, body_style))
    elements.append(Spacer(1, 12))

    # Experience
    elements.append(Paragraph("Professional Experience", header_style))
    for exp in data.get("experience", []):
        elements.append(Paragraph(f"<b>{exp['role']}</b> | {exp['company']}", body_style))
        elements.append(Paragraph(f"<i>{exp.get('duration', '')}</i>", body_style))
        
        bullets = [ListItem(Paragraph(b, body_style)) for b in exp.get("bullets", [])]
        if bullets:
            elements.append(ListFlowable(bullets, bulletType='bullet', leftIndent=20))
        elements.append(Spacer(1, 10))

    # Projects
    if data.get("projects"):
        elements.append(Paragraph("Key Projects", header_style))
        for proj in data.get("projects", []):
            elements.append(Paragraph(f"<b>{proj['name']}</b>", body_style))
            bullets = [ListItem(Paragraph(b, body_style)) for b in proj.get("bullets", [])]
            if bullets:
                elements.append(ListFlowable(bullets, bulletType='bullet', leftIndent=20))
            elements.append(Spacer(1, 8))

    # Education
    elements.append(Paragraph("Education", header_style))
    elements.append(Paragraph(data.get("education", ""), body_style))

    doc.build(elements)
    return file_path
