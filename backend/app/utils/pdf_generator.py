import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch

class PDFGenerator:
    """
    Utility to generate professional PDFs from tailored resume data.
    """
    def __init__(self, output_dir="static/resumes"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        # Custom styles for a clean, modern resume
        self.styles.add(ParagraphStyle(
            name='NameHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.indigo
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            color=colors.gray,
            spaceBefore=10,
            spaceAfter=6,
            borderWidth=0.5,
            borderColor=colors.lightgrey,
            borderPadding=2
        ))

    def generate_resume(self, data: dict, user_id: str, job_id: int) -> str:
        filename = f"resume_{user_id}_{job_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=LETTER)
        story = []

        # 1. Header (Placeholder for contact info in real app)
        story.append(Paragraph(data.get("full_name", "Candidate Name"), self.styles['NameHeader']))
        story.append(Spacer(1, 0.1 * inch))

        # 2. Summary
        story.append(Paragraph("Professional Summary", self.styles['SectionHeader']))
        story.append(Paragraph(data.get("summary", ""), self.styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        # 3. Skills
        story.append(Paragraph("Core Competencies", self.styles['SectionHeader']))
        skills = ", ".join(data.get("skills", []))
        story.append(Paragraph(skills, self.styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

        # 4. Experience
        story.append(Paragraph("Professional Experience", self.styles['SectionHeader']))
        for exp in data.get("experience", []):
            role_text = f"<b>{exp.get('role')}</b> at {exp.get('company')} ({exp.get('duration')})"
            story.append(Paragraph(role_text, self.styles['Normal']))
            
            bullets = [ListItem(Paragraph(b, self.styles['Normal'])) for b in exp.get("bullets", [])]
            story.append(ListFlowable(bullets, bulletType='bullet'))
            story.append(Spacer(1, 0.05 * inch))

        # 5. Education
        story.append(Paragraph("Education", self.styles['SectionHeader']))
        story.append(Paragraph(data.get("education", ""), self.styles['Normal']))

        doc.build(story)
        return os.path.abspath(filepath)

pdf_generator = PDFGenerator()
