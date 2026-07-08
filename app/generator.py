# app/generator.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_txt(content: str, output_path: str):
    """Writes plain text summary output."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def create_pdf(content: str, output_path: str):
    """Generates an A4 PDF using the LLM-generated title and summary content."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    body_style = ParagraphStyle(
        'A4SummaryBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        spaceAfter=12
    )
    
    title_style = ParagraphStyle(
        'A4SummaryTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        spaceAfter=20
    )

    # --- PARSE THE LLM TARGETED FORMAT ---
    pdf_title = "Executive Summary Report"
    remaining_content = content

    lines = content.split('\n')
    extracted_title = ""
    summary_lines = []

    for line in lines:
        if line.upper().startswith("TITLE:"):
            # Extract the title and strip markdown characters
            extracted_title = line[6:].replace('**', '').replace('#', '').strip()
        elif line.upper().startswith("SUMMARY:"):
            summary_lines.append(line[8:].strip())
        elif extracted_title:  # Capture subsequent summary lines if any
            summary_lines.append(line.strip())

    if extracted_title:
        pdf_title = extracted_title
    if summary_lines:
        remaining_content = "\n".join(summary_lines).strip()

    # Build structural document tree (Story)
    story = [
        Paragraph(pdf_title, title_style),
        Spacer(1, 15),
        Paragraph(remaining_content.replace("\n", "<br/>"), body_style)
    ]
    
    doc.build(story)