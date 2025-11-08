# components/export.py
import streamlit as st
import json
import base64
import os
from pathlib import Path
from report.generator import PDFReport
from report.word import generate_docx
from mailer.send import send_report
import tempfile

# =====================================================
# IMPORT CONFIG + UI (ÎNAINTE DE def render!)
# =====================================================
from config import (
    TITLE_COLOR, COVER_TITLE_COLOR, DEFAULT_SMTP,
    WATERMARK_TEXT, PAGE_HEADER_LOGO
)

# === UI CULOARE + WATERMARK (va fi în render, dar valorile vin din config) ===
# Acestea vor fi definite în render()

# =====================================================
# FUNCȚIA render()
# =====================================================
def render():
    st.subheader("Export & Import Project")

    # === WATERMARK DIN CONFIG (poți suprascrie în UI) ===
    add_watermark = st.checkbox("Add CONFIDENTIAL watermark", value=True)

    # === PDF STYLE SETTINGS (UI) ===
    st.subheader("PDF Style Settings")
    col1, col2 = st.columns(2)
    with col1:
        title_color = st.color_picker("Title Color (all sections)", TITLE_COLOR, key="title_color")
    with col2:
        cover_color = st.color_picker("Cover Title Color", COVER_TITLE_COLOR, key="cover_color")

    # === SALVARE PROIECT ===
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Project (.json)", type="secondary"):
            project_data = {
                "client": st.session_state.get("client", ""),
                "project": st.session_state.get("project", ""),
                "tester": st.session_state.get("tester", ""),
                "date": str(st.session_state.get("date", "")),
                "scope": st.session_state.get("scope", ""),
                "executive_summary_text": st.session_state.get("executive_summary_text", ""),
                "overview_text": st.session_state.get("overview_text", ""),
                "findings": st.session_state.findings,
                "poc_list": st.session_state.poc_list
            }
            json_str = json.dumps(project_data, indent=2, ensure_ascii=False)
            st.download_button("Download project.json", json_str, "project.json", "application/json")
            st.success("Project saved!")

    # === ÎNCĂRCARE PROIECT ===
    with col2:
        uploaded = st.file_uploader("Load Project (.json)", type="json")
        if uploaded and st.button("Import Project"):
            try:
                data = json.load(uploaded)
                for key in ["client", "project", "tester", "date", "scope", 
                           "executive_summary_text", "overview_text"]:
                    if key in data: st.session_state[key] = data[key]
                st.session_state.findings = data.get("findings", [])
                st.session_state.poc_list = data.get("poc_list", [])
                st.success("Project loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Import error: {e}")

    st.divider()

    # === GENERARE PDF (CU CULOARE DINAMICĂ) ===
# În interiorul def render() → după UI color picker
    if st.button("Generate PDF", type="primary"):
        try:
            logo_path = PAGE_HEADER_LOGO
            if not os.path.exists(logo_path):
                logo_path = None
    
            # === TRIMITE CULOAREA LA PDFReport ===
            pdf = PDFReport(
                logo_path=logo_path,
                watermark=add_watermark,
                title_color=title_color,     # ← DIN UI
                cover_color=cover_color      # ← DIN UI
            )
    
            pdf_bytes = pdf.generate(
                findings=st.session_state.findings,
                client=st.session_state.get("client", "Client"),
                project=st.session_state.get("project", "Project"),
                executive_text=st.session_state.get("executive_summary_text", ""),
                tester=st.session_state.get("tester", "N/A"),
                date=st.session_state.get("date"),
                scope=st.session_state.get("scope", ""),
                overview_text=st.session_state.get("overview_text", ""),
                poc_list=st.session_state.poc_list
            )
            st.download_button("Download PDF", pdf_bytes, "report.pdf", "application/pdf")
            st.success("PDF generat cu culori personalizate!")
        except Exception as e:
            st.error(f"Eroare PDF: {e}")

    # === GENERARE DOCX ===
    if st.button("Generate DOCX"):
        try:
            doc = generate_docx(st.session_state.findings, {"client": st.session_state.get("client"), "project": st.session_state.get("project")})
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                doc.save(tmp.name)
                docx_path = tmp.name
            with open(docx_path, "rb") as f:
                st.download_button("Download DOCX", f, "report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            os.unlink(docx_path)
            st.success("DOCX generated!")
        except Exception as e:
            st.error(f"DOCX error: {e}")

    st.divider()

    # === EMAIL UI (CU PRESETURI DIN CONFIG) ===
    st.subheader("Send Report via Email")
    with st.expander("SMTP Configuration", expanded=True):
        provider = st.selectbox("Provider", ["Gmail", "Yahoo", "Office365", "Custom"], key="email_provider")
        
        if provider in DEFAULT_SMTP:
            cfg = DEFAULT_SMTP[provider]
            smtp_server = cfg["server"]
            smtp_port = cfg["port"]
            use_tls = cfg["tls"]
            if "app_password_hint" in cfg:
                st.markdown(f"**App Password:** [{provider} App Passwords]({cfg['app_password_hint']})")
        else:
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com", key="smtp_server")
            smtp_port = st.number_input("Port", 1, 65535, 587, key="smtp_port")
            use_tls = st.checkbox("Use TLS", True, key="use_tls")

        email_user = st.text_input("Email (From)", key="email_user")
        email_pass = st.text_input("App Password / Password", type="password", key="email_pass")

    email_to = st.text_input("Recipient Email", key="email_to")

    if st.button("Send PDF + DOCX via Email", type="primary") and email_to and email_user and email_pass:
        with st.spinner("Sending..."):
            try:
                logo_path = PAGE_HEADER_LOGO
                if not os.path.exists(logo_path):
                    logo_path = None

                pdf = PDFReport(
                    logo_path=logo_path,
                    watermark=add_watermark,
                    title_color=title_color,
                    cover_color=cover_color
                )
                pdf_bytes = pdf.generate(
                    findings=st.session_state.findings,
                    client=st.session_state.get("client"),
                    project=st.session_state.get("project"),
                    executive_text=st.session_state.get("executive_summary_text"),
                    tester=st.session_state.get("tester"),
                    date=st.session_state.get("date"),
                    scope=st.session_state.get("scope"),
                    overview_text=st.session_state.get("overview_text"),
                    poc_list=st.session_state.poc_list
                )

                doc = generate_docx(st.session_state.findings, {"client": st.session_state.get("client"), "project": st.session_state.get("project")})

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(pdf_bytes)
                    pdf_path = tmp_pdf.name
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
                    doc.save(tmp_docx.name)
                    docx_path = tmp_docx.name

                success, msg = send_report(
                    email_to=email_to,
                    project_name=st.session_state.get("project", "Report"),
                    pdf_path=pdf_path,
                    docx_path=docx_path,
                    smtp_server=smtp_server,
                    smtp_port=smtp_port,
                    use_tls=use_tls,
                    email_user=email_user,
                    email_pass=email_pass
                )

                os.unlink(pdf_path)
                os.unlink(docx_path)

                if success:
                    st.success("Email trimis!")
                else:
                    st.error(f"Eroare: {msg}")

            except Exception as e:
                st.error(f"Eroare: {e}")
