# report/sections/legal.py
import streamlit as st  # ← IMPORT CRITIC
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch

def add_legal(pdf, client=None, **kwargs):
    # Preia client din session_state dacă nu e pasat
    client = client or st.session_state.get("client", "Client")

    pdf.story.append(Paragraph("Legal Disclaimer & Confidentiality", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 0.3 * inch))

    # === CONFIDENTIALITY STATEMENT ===
    conf_text = f"""
    <b>Confidentiality Statement</b><br/><br/>
    This report is strictly confidential and intended solely for the use of <b>{client}</b>. 
    It contains sensitive information regarding security vulnerabilities and should not be 
    disclosed to any third party without prior written consent.<br/><br/>
    
    Unauthorized distribution or reproduction may result in legal action.
    """
    pdf.story.append(Paragraph(conf_text, pdf.styles['Normal']))
    pdf.story.append(Spacer(1, 0.2 * inch))

    # === DISCLAIMER ===
    disclaimer = """
    <b>Disclaimer</b><br/><br/>
    The information provided is for informational purposes only. 
    No warranty is expressed or implied regarding accuracy or completeness.<br/><br/>
    
    The client is responsible for implementing remediation measures. 
    The testing team shall not be held liable for any damages.
    """
    pdf.story.append(Paragraph(disclaimer, pdf.styles['Normal']))
    pdf.story.append(Spacer(1, 0.3 * inch))

#    pdf.story.append(PageBreak())
