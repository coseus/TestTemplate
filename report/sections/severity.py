# report/sections/severity.py
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch

def add_severity_ratings(pdf, severity_data=None, **kwargs):
    # === TEXT ÎNAINTE DE TABEL ===
    pdf.story.append(Paragraph("Finding Severity Ratings", pdf.styles['SectionTitle']))
    intro_text = (
        "The following table defines levels of severity and corresponding CVSS score range that are used throughout the document "
        "to assess vulnerability and risk impact."
    )
    pdf.story.append(Paragraph(intro_text, pdf.styles['Normal']))
    pdf.story.append(Spacer(1, 0.2*inch))

    # === DEFAULT SEVERITY DATA ===
    if not severity_data:
        severity_data = [
            {"name": "Critical", "range": "9.0-10.0", "definition": "Exploitation is straightforward and usually results in system-level compromise."},
            {"name": "High", "range": "7.0-8.9", "definition": "Exploitation could cause elevated privileges and potentially a loss of data or downtime."},
            {"name": "Moderate", "range": "4.0-6.9", "definition": "Vulnerabilities exist but require extra steps such as social engineering."},
            {"name": "Low", "range": "0.1-3.9", "definition": "Non-exploitable but would reduce attack surface."},
            {"name": "Informational", "range": "N/A", "definition": "No vulnerability. Additional information provided."}
        ]

    # === TABEL SEVERITY ===
    colors_map = {
        "Critical": "#ffcccc", "High": "#ff9999", "Moderate": "#cc8800",
        "Low": "#90ee90", "Informational": "#add8e6"
    }

    data = [["Severity", "CVSS v3 Score Range", "Definition"]]
    for s in severity_data:
        data.append([
            Paragraph(f"<b>{s['name']}</b>", pdf.styles['Normal']),
            Paragraph(s['range'], pdf.styles['Normal']),
            Paragraph(s['definition'], pdf.styles['Normal'])
        ])

    table = Table(data, colWidths=[1.2*inch, 1.4*inch, 3.6*inch])
    style = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#87CEEB")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]

    for i, s in enumerate(severity_data, 1):
        style.append(('BACKGROUND', (0,i), (0,i), colors.HexColor(colors_map.get(s['name'], "#ffffff"))))
        style.append(('TEXTCOLOR', (0,i), (0,i), colors.black))
        style.extend([
            ('BACKGROUND', (1,i), (2,i), colors.HexColor("#2c3e50")),
            ('TEXTCOLOR', (1,i), (2,i), colors.white),
        ])

    table.setStyle(TableStyle(style))
    pdf.story.append(table)
    pdf.story.append(Spacer(1, 0.3*inch))

    # === TEXT DUPĂ TABEL – BOLD CORECT ===
    risk_text = (
        "<b>Risk Factors</b><br/>"
        "Risk is measured by two factors: <b>Likelihood</b> and <b>Impact</b>:<br/><br/>"
        "<b>Likelihood</b><br/>"
        "Likelihood measures the potential of a vulnerability being exploited. Ratings are given based on the difficulty of the attack, "
        "the available tools, attacker skill level, and client environment.<br/><br/>"
        "<b>Impact</b><br/>"
        "Impact measures the potential vulnerability’s effect on operations, including confidentiality, integrity, and availability "
        "of client systems and/or data, reputational harm, and financial loss."
    )
    pdf.story.append(Paragraph(risk_text, pdf.styles['Normal']))

    # Fără PageBreak() → rămâne pe pagina 4 cu Overview + Scope
