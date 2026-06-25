from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
import os


def generate_pdf(content: str, filename: str) -> str:
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/{filename}.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    for line in content.split("\n"):
        if line.strip() == "":
            story.append(Spacer(1, 4 * mm))
        else:
            story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    return output_path
