# report/sections/cover.py
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

def add_cover(pdf, client=None, project=None, tester=None, date=None, **kwargs):
    client = client or "Client Name"
    project = project or "Project Name"
    tester = tester or "Security Analyst"
    date = date or "November 2025"

    # === GRADIENT BACKGROUND – 70% DIN PAGINĂ (MAI MARE) ===
    page_height = pdf.doc.height + pdf.doc.topMargin + pdf.doc.bottomMargin
    gradient_height = page_height * 0.70  # 70% din pagină

    gradient_data = [[""]]
    gradient = Table(
        gradient_data,
        colWidths=[pdf.doc.width + pdf.doc.leftMargin + pdf.doc.rightMargin],
        rowHeights=[gradient_height]
    )
    gradient.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#1e40af")),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 0),
        ('TOPPADDING', (0,0), (0,0), 0),
        ('BOTTOMPADDING', (0,0), (0,0), 0),
    ]))
    pdf.story.append(gradient)
    pdf.story.append(Spacer(1, -gradient_height))

    # === LOGO COVER – CENTRAT ===
    cover_logo_path = os.path.join("assets", "cover_logo.png")
    if os.path.exists(cover_logo_path):
        try:
            logo = Image(cover_logo_path, width=2.8*inch, height=1.4*inch)
            logo.hAlign = 'CENTER'
            pdf.story.append(logo)
        except Exception as e:
            print(f"Cover logo error: {e}")
    else:
        fallback_path = os.path.join("assets", "logo.png")
        if os.path.exists(fallback_path):
            try:
                logo = Image(fallback_path, width=2.2*inch, height=1.1*inch)
                logo.hAlign = 'CENTER'
                pdf.story.append(logo)
            except:
                pass
    pdf.story.append(Spacer(1, 0.6*inch))

    # === TITLU PRINCIPAL (CENTRAT) ===
    title_para = Paragraph("Penetration Test Report", pdf.styles['CoverTitle'])
    title_para.hAlign = 'CENTER'
    pdf.story.append(title_para)
    pdf.story.append(Spacer(1, 0.3*inch))

    # === PROJECT NAME – CENTRAT, MAI JOS, BOLD, MARE ===
    project_para = Paragraph(
        f"<font size=18 color='#e2e8f0'><b>{project}</b></font>",
        pdf.styles['Normal']
    )
    project_para.hAlign = 'CENTER'
    pdf.story.append(project_para)
    pdf.story.append(Spacer(1, 2.2*inch))  # ↓ MUTAT MAI JOS

    # === DETALII CLIENT – CENTRAT, ALB ===
    details = f"""
    <font size=13 color='#e2e8f0'>
    <b>Client:</b> {client}<br/>
    <b>Tester:</b> {tester}<br/>
    <b>Date:</b> {date}<br/>
    </font>
    """
    details_para = Paragraph(details, pdf.styles['Normal'])
    details_para.hAlign = 'CENTER'
    pdf.story.append(details_para)
    pdf.story.append(Spacer(1, 0.8*inch))

    # === CONFIDENTIAL – CENTRAT JOS ===
    conf_para = Paragraph("CONFIDENTIAL", pdf.styles['Confidential'])
    conf_para.hAlign = 'CENTER'
    pdf.story.append(conf_para)

    pdf.story.append(PageBreak())
    if pdf.watermark:
        from config import WATERMARK_TEXT, WATERMARK_COLOR, WATERMARK_FONTSIZE, WATERMARK_ANGLE
        pdf.story.append(Paragraph(
            f"<font color='{WATERMARK_COLOR}' size={WATERMARK_FONTSIZE}>{WATERMARK_TEXT}</font>",
            pdf.styles['Watermark']
        ))
