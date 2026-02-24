import os
import html
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def md_text_to_flowables(md_text: str):
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="LogTitle",
        parent=styles["Title"],
        fontSize=18,
        spaceAfter=10,
        textColor=colors.HexColor("#1f2d3d"),
    )
    week_style = ParagraphStyle(
        name="WeekHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#0b5394"),
    )
    entry_style = ParagraphStyle(
        name="Entry",
        parent=styles["BodyText"],
        fontSize=10,
        leading=13,
        spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        name="Meta",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        textColor=colors.grey,
        spaceAfter=6,
    )

    flow = []

    lines = md_text.splitlines()

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped == "":
            flow.append(Spacer(1, 6))
            continue

        if stripped.startswith("# "):
            text = html.escape(stripped[2:].strip())
            flow.append(Paragraph(text, title_style))
            continue

        if stripped.startswith("## "):
            text = html.escape(stripped[3:].strip())
            flow.append(Paragraph(text, week_style))
            continue

        if stripped == "---":
            flow.append(Spacer(1, 10))
            continue

        # Keep bold markers as plain text; Paragraph supports simple inline markup but we avoid relying on it.
        safe = html.escape(stripped)

        # Slightly dim meta lines like Project/Period headers
        if safe.lower().startswith("project:") or safe.lower().startswith("period:") or safe.lower().startswith("intern roles"):
            flow.append(Paragraph(safe, meta_style))
        else:
            flow.append(Paragraph(safe, entry_style))

    return flow


def build_pdf_from_md(md_path: str, out_pdf_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    os.makedirs(os.path.dirname(out_pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        out_pdf_path,
        pagesize=A4,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
        title="Internship Daily Logbook - Governance Weekly",
        author="Governance Weekly Interns",
    )

    flow = md_text_to_flowables(md_text)
    doc.build(flow)


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path = os.path.join(base_dir, "INTERNSHIP_DAILY_LOGBOOK.md")

    out_name = "Internship_Daily_Logbook_2025-11-07_to_2025-12-27.pdf"
    out_pdf_path = os.path.join(base_dir, "output", out_name)

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Missing logbook markdown: {md_path}")

    build_pdf_from_md(md_path, out_pdf_path)
    print(f"PDF created: {out_pdf_path}")


if __name__ == "__main__":
    main()
