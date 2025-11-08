# report/sections/overview.py
import streamlit as st
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

from reportlab.platypus import Paragraph

def add_overview(pdf, **kwargs):
    overview_text = st.session_state.get("overview_text", "No overview provided.")
    pdf.story.append(Paragraph("<b>Assessment Overview</b>", pdf.styles['Heading2']))
    pdf.story.append(Paragraph(overview_text, pdf.styles['Normal']))
    pdf.story.append(Paragraph("<br/>", pdf.styles['Normal']))

'''
def add_overview(pdf, overview_text=None, **kwargs):
    overview_text = overview_text or st.session_state.get("overview_text", "No overview provided.")
    
    pdf.story.append(Paragraph("Assessment Overview", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.2 * inch))
    
    # Split în paragrafe
    paragraphs = [p.strip() for p in overview_text.split("\n") if p.strip()]
    for para in paragraphs:
        pdf.story.append(Paragraph(para, pdf.styles['Normal']))
        pdf.story.append(Spacer(1, 0.1 * inch))
    
    pdf.story.append(PageBreak())
'''
