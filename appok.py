import streamlit as st
from datetime import datetime
import base64
from report.pdf_generator import generate_pdf_bytes
from report.docx_generator import generate_docx_bytes
from report.parsers import parse_nessus_xml, parse_nmap_xml
from report.data_model import ReportData

st.set_page_config(page_title="Pentest Report Modular", layout="wide", page_icon="🛡️")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.block-container { max-width: 1200px; padding-top: 1rem; padding-bottom: 2rem; }
h1 { text-align: center; font-size: 2.2rem !important; font-weight: 800 !important; color: #90CAF9 !important; }
h2, h3 { color: #A5D6A7 !important; }
.badge {
    display:inline-block; padding:2px 8px; border-radius:8px; font-size:0.8rem; font-weight:600; color:white;
}
.badge-critical { background:#CC3333; }
.badge-high { background:#FF8C33; }
.badge-moderate { background:#E6B800; color:black; }
.badge-low { background:#3399FF; }
.badge-info { background:#999999; }
.stTextInput>div>div>input, .stTextArea textarea {
    background-color:#1E1E1E !important; color:#FFFFFF !important;
    border:1px solid #444 !important; border-radius:8px !important;
    font-size:16px !important; padding:10px !important;
}
div.stButton > button:first-child {
    background-color:#2E7D32 !important; color:white !important;
    border-radius:8px !important; padding:0.6rem 1.4rem !important;
    font-weight:600; border:none;
}
div.stButton > button:first-child:hover { background-color:#388E3C !important; }
.stDownloadButton > button {
    background-color:#1565C0 !important; color:white !important;
    border-radius:8px !important; padding:0.5rem 1.2rem !important; border:none;
}
.stDownloadButton > button:hover { background-color:#1976D2 !important; }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "report" not in st.session_state:
    st.session_state.report = ReportData.default()
r = st.session_state.report

# ---------- HEADER ----------
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/Shield_icon_2022.svg", width=80)
with col_title:
    st.title("🛡️ Pentest Report Modular")

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 General Info", 
    "📄 Scope & Details", 
    "🔍 Findings", 
    "📤 Export"
])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("General Information")
    c1, c2 = st.columns(2)
    with c1:
        r["client"] = st.text_input("Client", r.get("client", ""))
        r["project"] = st.text_input("Project", r.get("project", ""))
        r["tester"] = st.text_input("Tester", r.get("tester", ""))
    with c2:
        r["contact"] = st.text_input("Contact Email", r.get("contact", ""))
        r["date"] = st.date_input("Date", datetime.today())
        r["version"] = st.text_input("Version", r.get("version", "1.0"))

    r["executive_summary"] = st.text_area("Executive Summary", r.get("executive_summary", ""), height=160)

    st.subheader("Contact Information")
    contact_cols = st.columns([2, 2, 2])
    with contact_cols[0]:
        name = st.text_input("Name", key="contact_name")
    with contact_cols[1]:
        title = st.text_input("Title", key="contact_title")
    with contact_cols[2]:
        contact_info = st.text_input("Contact Info", key="contact_info")
    if st.button("➕ Add Contact"):
        if "contacts" not in r:
            r["contacts"] = []
        r["contacts"].append({"name": name, "title": title, "contact": contact_info})
        st.success("Contact added.")
    if r.get("contacts"):
        st.table(r["contacts"])

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Assessment Details & Scope")
    r["assessment_details"] = st.text_area("Assessment Details", r.get("assessment_details", ""), height=140)
    r["scope"] = st.text_area("Scope", r.get("scope", ""), height=140)
    r["scope_exclusions"] = st.text_area("Scope Exclusions", r.get("scope_exclusions", ""), height=140)
    r["client_allowances"] = st.text_area("Client Allowances", r.get("client_allowances", ""), height=140)

# ---------- TAB 3 ----------
with tab3:
    st.subheader("Findings Management")

    # --- IMPORT AUTOMAT ---
    st.markdown("### 🧩 Import from Nessus / Nmap")
    nfile = st.file_uploader("Upload Nessus XML", type=["nessus", "xml"], key="nessus")
    mfile = st.file_uploader("Upload Nmap XML", type=["xml"], key="nmap")
    if nfile:
    	parsed_nessus = parse_nessus_xml(nfile.read())
    	if parsed_nessus:
        	if "findings" not in r:
            		r["findings"] = []
        	r["findings"].extend(parsed_nessus)
        	st.success(f"✅ Imported {len(parsed_nessus)} findings from Nessus.")
    	else:
        	st.warning("No findings detected in Nessus file.")

    if mfile:
    	parsed_nmap = parse_nmap_xml(mfile.read())
    	if parsed_nmap:
        	if "findings" not in r:
            		r["findings"] = []
        	r["findings"].extend(parsed_nmap)
        	st.success(f"✅ Imported {len(parsed_nmap)} findings from Nmap.")
    	else:
        	st.warning("No findings detected in Nmap file.")

    # --- ADAUGARE MANUALA ---
    st.markdown("### ✏️ Add Finding Manually")
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        f_title = st.text_input("Title")
        f_sev = st.selectbox("Severity", ["Critical", "High", "Moderate", "Low", "Informational"])
        f_cvss = st.text_input("CVSS Score")
    with fcol2:
        f_desc = st.text_area("Description")
        f_reco = st.text_area("Recommendation")
    f_term = st.text_area("Terminal Output / Commands (optional)")

    f_imgs = st.file_uploader("Attach Evidence Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    f_txts = st.file_uploader("Attach Evidence Text Files", type=["txt"], accept_multiple_files=True)

    if st.button("➕ Add Finding"):
        entry = {
            "id": f"F-{len(r['findings'])+1}",
            "title": f_title,
            "severity": f_sev,
            "cvss": f_cvss,
            "description": f_desc,
            "recommendation": f_reco,
            "terminal_output": f_term,
            "evidence_images": [],
            "evidence_texts": [],
        }
        for f in f_imgs:
            entry["evidence_images"].append(base64.b64encode(f.read()).decode())
        for t in f_txts:
            entry["evidence_texts"].append(t.read().decode(errors="ignore"))
        r["findings"].append(entry)
        st.success("✅ Finding added manually.")

    # --- LISTA CU FILTRE SI BADGES ---
    if r.get("findings"):
        st.markdown("### 📊 All Findings")
        sev_filter = st.multiselect(
            "Filter by Severity",
            ["Critical", "High", "Moderate", "Low", "Informational"],
            default=["Critical", "High", "Moderate", "Low", "Informational"]
        )

        for f in [f for f in r["findings"] if f["severity"] in sev_filter]:
            color_class = {
                "Critical": "critical",
                "High": "high",
                "Moderate": "moderate",
                "Low": "low",
                "Informational": "info"
            }.get(f["severity"], "info")
            st.markdown(
                f"<span class='badge badge-{color_class}'>{f['severity']}</span> "
                f"**{f['title']}**", unsafe_allow_html=True
            )
            with st.expander("Details"):
                st.write(f"**CVSS:** {f['cvss']}")
                st.write(f"**Description:** {f['description']}")
                st.write(f"**Recommendation:** {f['recommendation']}")
                if f.get("terminal_output"):
                    st.code(f["terminal_output"], language="bash")

    # --- ADDITIONAL REPORTS ---
    st.markdown("### 🧾 Additional Reports & Scans (Informational)")
    ar_title = st.text_input("Report Title")
    ar_desc = st.text_area("Description / Notes")
    if st.button("➕ Add Additional Report"):
        if "additional_reports" not in r:
            r["additional_reports"] = []
        r["additional_reports"].append({"title": ar_title, "description": ar_desc})
        st.success("Added to Additional Reports.")
    if r.get("additional_reports"):
        for ar in r["additional_reports"]:
            st.markdown(f"**{ar['title']}**\n\n{ar['description']}")

# ---------- TAB 4 ----------
# ---------- TAB 4 ----------
with tab4:
    st.subheader("Generate and Download Report")

    # Watermark option
    add_wm = st.checkbox("Add Confidential Watermark", value=False)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📄 Generate PDF Report"):
            pdf_bytes = generate_pdf_bytes(r, watermark="CONFIDENTIAL" if add_wm else None)
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_bytes,
                file_name=f"report_{r.get('client','')}.pdf",
                mime="application/pdf"
            )
            b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

    with c2:
        if st.button("📝 Generate DOCX Report"):
            docx_bytes = generate_docx_bytes(r, watermark="CONFIDENTIAL" if add_wm else None)
            st.download_button(
                "⬇️ Download DOCX",
                data=docx_bytes,
                file_name=f"report_{r.get('client','')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
