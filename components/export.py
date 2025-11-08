# components/export.py
import streamlit as st
import json
import os
from pathlib import Path
from report.generator import PDFReport
from report.word import generate_docx
from mailer.send import send_report
import tempfile

def render():
    st.subheader("Export & Import Project")
    add_watermark = st.checkbox("Add CONFIDENTIAL watermark on all pages", value=True)

    col1, col2 = st.columns(2)

    # === SALVARE PROIECT ===
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
                "poc_list": st.session_state.poc_list,
                "contacts": st.session_state.get("contacts", [])
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
                           "executive_summary_text", "overview_text", "contacts"]:
                    if key in data:
                        st.session_state[key] = data[key]
                st.session_state.findings = data.get("findings", [])
                st.session_state.poc_list = data.get("poc_list", [])
                st.success("Project loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Import error: {e}")

    st.divider()

    # === GENERARE PDF ===
    if st.button("Generate PDF", type="primary"):
        try:
            # === DEFINĂ LOGO_PATH CORECT ===
            base_path = Path(__file__).parent.parent
            logo_path = base_path / "assets" / "logo.png"
            logo_path = str(logo_path) if logo_path.exists() else None  # ← FIXAT

            pdf = PDFReport(logo_path=logo_path, watermark=add_watermark)
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
            pdf_filename = f"{st.session_state.get('project', 'report').replace(' ', '_')}_report.pdf"
            st.download_button("Download PDF", pdf_bytes, pdf_filename, "application/pdf")
            st.success("PDF generated!")
        except Exception as e:
            st.error(f"PDF error: {e}")

    # === GENERARE DOCX ===
    if st.button("Generate DOCX"):
        try:
            doc = generate_docx(
                findings=st.session_state.findings,
                project_info={
                    "client": st.session_state.get("client", "Client"),
                    "project": st.session_state.get("project", "Project")
                }
            )
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                doc.save(tmp.name)
                docx_path = tmp.name
            with open(docx_path, "rb") as f:
                st.download_button(
                    "Download DOCX",
                    f,
                    f"{st.session_state.get('project', 'report').replace(' ', '_')}_report.docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            st.success("DOCX generated!")
            os.unlink(docx_path)
        except Exception as e:
            st.error(f"DOCX error: {e}")

    st.divider()

    # components/export.py (doar secțiunea EMAIL)
    # components/export.py (secțiunea EMAIL)

    st.subheader("Send Report via Email")
    
    # === 1. UI CONFIG SMTP (ÎNTOTDEAUNA VIZIBIL) ===
    with st.expander("SMTP Configuration", expanded=True):
        provider = st.selectbox("Provider", ["Gmail", "Yahoo", "Office365", "Custom"], key="email_provider")
    
        # === SETĂRI AUTOMATE ===
        if provider == "Gmail":
            smtp_server = "smtp.gmail.com"
            smtp_port = st.radio("Port", [587, 465], index=0, key="port_gmail")
            use_tls = smtp_port == 587
            st.markdown("**App Password:** [google.com/apppasswords](https://myaccount.google.com/apppasswords)")
        elif provider == "Yahoo":
            smtp_server = "smtp.mail.yahoo.com"
            smtp_port = 587
            use_tls = True
            st.markdown("**App Password:** [Yahoo App Passwords](https://login.yahoo.com/myaccount/app-passwords)")
        elif provider == "Office365":
            smtp_server = "smtp.office365.com"
            smtp_port = 587
            use_tls = True
        else:
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com", key="smtp_server_custom")
            smtp_port = st.number_input("Port", 1, 65535, 587, key="smtp_port_custom")
            use_tls = st.checkbox("Use TLS", True, key="use_tls_custom")
    
        # === CREDENȚIALE (OBLIGATORIU DEFINITE) ===
        email_user = st.text_input("Email (From)", value="", key="email_user", placeholder="you@gmail.com")
        email_pass = st.text_input("App Password / Password", type="password", key="email_pass")
    
    # === 2. DESTINATAR ===
    email_to = st.text_input("Recipient Email", placeholder="client@company.com", key="email_to")
    
    # === 3. BUTON TRIMITE ===
    if st.button("Send PDF + DOCX via Email", type="primary"):
        # === VALIDARE ===
        if not email_to.strip():
            st.error("Introdu destinatarul!")
        elif not email_user.strip():
            st.error("Introdu emailul expeditor!")
        elif not email_pass.strip():
            st.error("Introdu App Password!")
        else:
            with st.spinner("Generare + trimitere..."):
                try:
                    # === GEN PDF ===
                    logo_path = str(Path(__file__).parent.parent / "assets" / "logo.png") if (Path(__file__).parent.parent / "assets" / "logo.png").exists() else None
                    pdf = PDFReport(logo_path=logo_path, watermark=add_watermark)
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
    
                    # === GEN DOCX ===
                    doc = generate_docx(st.session_state.findings, {"client": st.session_state.get("client"), "project": st.session_state.get("project")})
    
                    # === SALVEAZĂ TEMPORAR ===
                    import tempfile, os
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                        f.write(pdf_bytes)
                        pdf_path = f.name
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as f:
                        doc.save(f.name)
                        docx_path = f.name
    
                    # === TRIMITE EMAIL ===
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
    
                    # === CURĂȚĂ ===
                    for p in [pdf_path, docx_path]:
                        if os.path.exists(p):
                            os.unlink(p)
    
                    if success:
                        st.success("Email trimis cu succes!")
                    else:
                        st.error(f"Eroare: {msg}")
    
                except Exception as e:
                    st.error(f"Eroare neașteptată: {e}")
                    # Curăță fișierele
                    for p in [pdf_path, docx_path] if 'pdf_path' in locals() else []:
                        if os.path.exists(p):
                            os.unlink(p)