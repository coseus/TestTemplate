# report/sections/contact.py
import streamlit as st
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch

def add_contact_section(pdf, **kwargs):
    """Adaugă tabelul dinamic de contacte în PDF"""
    contacts = st.session_state.get("contacts", [])
    
    if not contacts:
        pdf.story.append(Paragraph("<b>Contact Information</b>", pdf.styles['SectionTitle']))
        pdf.story.append(Paragraph("No contacts defined.", pdf.styles['Normal']))
        return

    # Header
    data = [
        [Paragraph("<b>Contact Information</b>", pdf.styles['Heading2'])],
        [""],
        ["Name", "Role", "Email", "Type"]
    ]

    # Rows
    for c in contacts:
        data.append([
            c.get("name", "N/A"),
            c.get("role", "N/A"),
            c.get("email", "N/A"),
            c.get("type", "N/A")
        ])

    table = Table(data, colWidths=[2.0*inch, 2.0*inch, 2.4*inch, 1.6*inch])
    table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E4057")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor("#E5E7E9")),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 2), (-1, 2), 11),
        ('GRID', (0, 2), (-1, -1), 0.5, colors.HexColor("#D5D8DC")),
        ('FONTNAME', (0, 3), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 3), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, 1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
    ]))
    pdf.story.append(table)
    pdf.story.append(Paragraph("<br/>", pdf.styles['Normal']))
