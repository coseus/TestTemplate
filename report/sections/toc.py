# report/sections/toc.py
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch

def severity_color(sev):
    return {
        "Critical": "#dc2626",
        "High": "#f97316",
        "Moderate": "#facc15",
        "Low": "#10b981",
        "Informational": "#6366f1"
    }.get(sev, "#000000")

def add_toc(pdf, findings=None, poc_list=None, **kwargs):
    findings = findings or []
    poc_list = poc_list or []

    pdf.story.append(Paragraph("Table of Contents", pdf.styles['SectionTitle']))
    pdf.story.append(Spacer(1, 0.3 * inch))

    data = [["Page", "Section", "Details"]]

    # === SECȚIUNI FIXE (FĂRĂ 7) ===
    fixed_sections = [
        ("1", "Cover Page", ""),
        ("2", "Table of Contents", ""),
        ("3", "Legal Disclaimer & Contact", ""),
        ("4", "Assessment Overview", ""),
        ("4", "Scope of Testing", ""),
        ("4", "Severity Ratings", ""),
        ("5", "Executive Summary", ""),
        ("6", "Technical Findings", ""),   # ← 6
    ]

    for page, section, detail in fixed_sections:
        data.append([page, section, detail])

    # === FINDINGS → 6.1, 6.2 (INDENTAT CU 4 SPAȚII) ===
    order = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3, "Informational": 4}
    sorted_findings = sorted(findings, key=lambda f: order.get(f.get("severity", ""), 5))

    for i, f in enumerate(sorted_findings, 1):
        fid = f.get("id", "VULN")
        short = (f.get("title", "")[:38] + "...") if len(f.get("title", "")) > 38 else f.get("title", "")
        colored = Paragraph(f"    <font color='{severity_color(f.get('severity', ''))}'>{fid} - {short}</font>", pdf.styles['Normal'])
        data.append([f"6.{i}", colored, f.get("severity", "")])  # ← 6.1 INDENTAT

    # === 7. Steps to Reproduce ===
    data.append(["7", "Steps to Reproduce", ""])

    # === POC → 7.1, 7.2 (INDENTAT CU 4 SPAȚII) ===
    for i, poc in enumerate(poc_list, 1):
        title = poc.get("title", f"PoC {i}")
        data.append([f"7.{i}", f"    {title}", ""])  # ← 7.1 INDENTAT

    # === TABEL TOC ===
    table = Table(data, colWidths=[0.8*inch, 4.5*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    pdf.story.append(table)
