# report/sections/findings.py
from reportlab.platypus import Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import base64

# === CULOARE SEVERITATE ===
def severity_color(severity):
    """Return hex color for severity level"""
    colors_map = {
        "Critical": "#8B0000",      # Dark Red
        "High": "#FF4500",          # Orange Red
        "Moderate": "#FFD700",      # Gold
        "Low": "#32CD32",           # Lime Green
        "Informational": "#1E90FF"  # Dodger Blue
    }
    return colors_map.get(severity, "#000000")  # Black default

def add_technical_findings(pdf, findings=None, **kwargs):
    findings = findings or []
    pdf.story.append(Paragraph("6. Technical Findings", pdf.styles['SectionTitle']))
    pdf.story.append(Spacer(1, 0.2 * inch))

    for i, f in enumerate(findings, 1):
        # === TITLU + ID + HOST ===
        pdf.story.append(Paragraph(
            f"<b>6.{i} {f.get('id', 'N/A')} - {f.get('title', 'No Title')}</b>",
            pdf.styles['Heading2']
        ))
        pdf.story.append(Paragraph(f"<b>Host:</b> {f.get('host', 'N/A')}", pdf.styles['Normal']))
        pdf.story.append(Paragraph(f"<b>CVSS:</b> {f.get('cvss', 'N/A')}", pdf.styles['Normal']))

        # === SEVERITATE CU CULOARE ===
        sev = f.get('severity', 'Unknown')
        pdf.story.append(Paragraph(
            f"<b>Severity:</b> <font color='{severity_color(sev)}'>{sev}</font>",
            pdf.styles['Normal']
        ))

        # === DESCRIERE ===
        description = f.get('description', '')
        if description:
            pdf.story.append(Paragraph(description, pdf.styles['Normal']))
        pdf.story.append(Spacer(1, 0.1 * inch))

        # === CODE BLOCK – STIL TERMINAL (NEGRU + VERDE) ===
        code = f.get('code', '').strip()
        if code:
            pdf.story.append(Paragraph("<b>Proof of Concept (Terminal):</b>", pdf.styles['Normal']))

            # Split în linii
            code_lines = code.split('\n')
            if not code_lines:
                code_lines = [""]

            # Creează tabel cu fundal negru
            code_data = []
            for line in code_lines:
                # Escape HTML special chars
                safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                code_data.append([Paragraph(
                    f"<font face='Courier' size=8 color='#00FF00'>{safe_line}</font>",
                    pdf.styles['Normal']
                )])

            code_table = Table(code_data, colWidths=[6.5 * inch])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#000000")),  # NEGRU
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#00FF00")),   # VERDE
                ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#333333")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEADING', (0, 0), (-1, -1), 10),
            ]))
            pdf.story.append(code_table)
            pdf.story.append(Spacer(1, 0.2 * inch))

        # === IMAGINI ===
        for img_b64 in f.get('images', []):
            try:
                # Extrage doar bytes
                header, b64_data = img_b64.split(',', 1)
                img_bytes = base64.b64decode(b64_data)
                img_stream = io.BytesIO(img_bytes)

                img = RLImage(img_stream, width=6 * inch, height=3 * inch)
                img.hAlign = 'CENTER'
                pdf.story.append(img)
                pdf.story.append(Spacer(1, 0.2 * inch))
            except Exception as e:
                pdf.story.append(Paragraph(f"[Image load error: {str(e)}]", pdf.styles['Normal']))

        # === REMEDIATION ===
        remediation = f.get('remediation', '')
        if remediation:
            pdf.story.append(Paragraph(f"<b>Remediation:</b> {remediation}", pdf.styles['Normal']))

        pdf.story.append(Spacer(1, 0.4 * inch))
