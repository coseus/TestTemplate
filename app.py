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
# ---------- TAB 2 ----------
with tab3:
    st.subheader("Findings Management")

    # Upload Nessus & Nmap
    st.markdown("### 📥 Import Findings")
    nfile = st.file_uploader("Upload Nessus (.nessus)", type=["nessus"], key="nessus")
    mfile = st.file_uploader("Upload Nmap XML (.xml)", type=["xml"], key="nmap")

    if nfile:
        parsed_nessus = parse_nessus_xml(nfile.read())
        if parsed_nessus:
            r.setdefault("findings", []).extend(parsed_nessus)
            st.success(f"✅ Imported {len(parsed_nessus)} findings from Nessus.")
        else:
            st.warning("⚠️ No findings detected in Nessus file.")

    if mfile:
        parsed_nmap = parse_nmap_xml(mfile.read())
        if parsed_nmap:
            r.setdefault("findings", []).extend(parsed_nmap)
            st.success(f"✅ Imported {len(parsed_nmap)} findings from Nmap.")
        else:
            st.warning("⚠️ No findings detected in Nmap file.")

    st.markdown("---")

    # Manual Finding Input
    st.markdown("### ✍️ Add Manual Finding")
    with st.form("manual_finding_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fid = st.text_input("Finding ID", placeholder="e.g. MANUAL-001")
            title = st.text_input("Finding Title", placeholder="e.g. Weak SSH Configuration")
            severity = st.selectbox("Severity", ["Critical", "High", "Moderate", "Low", "Informational"])
        with col2:
            cvss = st.text_input("CVSS Score", placeholder="e.g. 7.5")
            desc = st.text_area("Description", height=100)
            rec = st.text_area("Recommendation", height=100)

        terminal = st.text_area("Terminal Output / Commands (optional)", height=120)

        # Upload evidence
        st.markdown("### 📎 Attach Evidence (optional)")
        images = st.file_uploader("Upload screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="img_upload")
        txt_files = st.file_uploader("Upload text/log evidence", type=["txt", "log"], accept_multiple_files=True, key="txt_upload")

        submitted = st.form_submit_button("➕ Add Finding")

        if submitted:
            img_b64 = []
            for img in images or []:
                img_b64.append(base64.b64encode(img.read()).decode("utf-8"))

            txt_content = []
            for tfile in txt_files or []:
                txt_content.append(tfile.read().decode("utf-8", errors="ignore"))

            r.setdefault("findings", []).append({
                "id": fid or f"MANUAL-{len(r.get('findings', [])) + 1}",
                "title": title or "Untitled Finding",
                "severity": severity,
                "cvss": cvss,
                "description": desc,
                "recommendation": rec,
                "terminal_output": terminal,
                "evidence_images": img_b64,
                "evidence_texts": txt_content
            })
            st.success("✅ Manual finding added successfully!")

    findings = r.get("findings", [])
    if not findings:
        st.info("📭 No findings available yet.")
    else:
        st.markdown("---")

        # ---- Severity summary ----
        sev_order = ["Critical", "High", "Moderate", "Low", "Informational"]
        sev_colors = {"Critical": "🟥", "High": "🟧", "Moderate": "🟨", "Low": "🟦", "Informational": "⚪"}
        sev_counts = {s: sum(1 for f in findings if f["severity"] == s) for s in sev_order}
        st.markdown(" ".join(f"{sev_colors[s]} **{s}**: {sev_counts[s]}" for s in sev_order if sev_counts[s] > 0))

        import plotly.express as px
        sev_chart = px.bar(
            x=list(sev_counts.keys()), y=list(sev_counts.values()),
            color=list(sev_counts.keys()),
            color_discrete_map={
                "Critical": "crimson", "High": "darkorange", "Moderate": "gold",
                "Low": "deepskyblue", "Informational": "lightgrey"
            },
            title="Findings by Severity", labels={"x": "Severity", "y": "Count"}
        )
        sev_chart.update_layout(showlegend=False, height=300)
        st.plotly_chart(sev_chart, width="stretch")

        # ---- Filter ----
        sev_filter = st.multiselect("Filter findings by severity", sev_order, default=sev_order)
        filtered = [f for f in findings if f["severity"] in sev_filter]
        st.write(f"### Showing {len(filtered)} findings:")

        for f in filtered:
            st.markdown(
                f"""
                <div style="border:1px solid #444; border-radius:8px; padding:10px; margin-bottom:10px;">
                <b>{sev_colors[f["severity"]]} {f["severity"]}</b> — <b>{f["title"]}</b><br>
                <small>ID: {f["id"]} | CVSS: {f.get("cvss","N/A")}</small><br><br>
                <details>
                    <summary><b>Description</b></summary>
                    <pre style="white-space:pre-wrap;">{f.get("description","")}</pre>
                </details>
                <details>
                    <summary><b>Recommendation</b></summary>
                    <pre style="white-space:pre-wrap;">{f.get("recommendation","")}</pre>
                </details>
                <details>
                    <summary><b>Terminal Output / Commands</b></summary>
                    <pre style="white-space:pre-wrap; background-color:#111; color:#0f0; padding:10px; border-radius:5px;">{f.get("terminal_output","")}</pre>
                </details>
                </div>
                """, unsafe_allow_html=True
            )

        # ---- Manage / Delete findings ----
        st.markdown("---")
        st.subheader("🧹 Manage Imported Findings")

        if filtered:
            delete_mode = st.radio(
                "Select deletion mode:",
                ["Delete by Selection", "Delete by Severity"],
                horizontal=True,
            )

            if delete_mode == "Delete by Selection":
                selected_titles = st.multiselect(
                    "Select findings to delete:",
                    [f"{f['id']} - {f['title']}" for f in filtered],
                )
                if selected_titles:
                    confirm = st.checkbox("✅ Yes, I confirm deletion of selected findings")
                    if st.button("🗑️ Delete Selected Findings"):
                        if confirm:
                            before_count = len(r["findings"])
                            r["findings"] = [
                                f for f in r["findings"]
                                if f"{f['id']} - {f['title']}" not in selected_titles
                            ]
                            removed = before_count - len(r["findings"])
                            st.success(f"✅ Removed {removed} findings successfully.")
                        else:
                            st.warning("⚠️ Please confirm deletion first.")

            elif delete_mode == "Delete by Severity":
                delete_sevs = st.multiselect("Select severities to delete:", sev_order)
                if delete_sevs:
                    confirm2 = st.checkbox("✅ Yes, I confirm deletion by severity")
                    if st.button("🗑️ Delete by Severity"):
                        if confirm2:
                            before_count = len(r["findings"])
                            r["findings"] = [
                                f for f in r["findings"] if f["severity"] not in delete_sevs
                            ]
                            removed = before_count - len(r["findings"])
                            st.success(f"✅ Removed {removed} findings by severity.")
                        else:
                            st.warning("⚠️ Please confirm deletion first.")
        else:
            st.info("No findings available to manage or delete.")

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
with tab4:
    st.subheader("Generate and Download Report")

    # Watermark option
    add_wm = st.checkbox("Add Confidential Watermark", value=False)

    # Export filter option
    st.markdown("### 🎯 Export Filter")
    sev_export_filter = st.multiselect(
        "Select which severities to include in exported report (leave empty for all):",
        ["Critical", "High", "Moderate", "Low", "Informational"],
    )

    # Build filtered findings for export
    findings_to_export = r.get("findings", [])
    if sev_export_filter:
        findings_to_export = [
            f for f in r.get("findings", [])
            if f["severity"] in sev_export_filter
        ]
        st.info(f"🧾 {len(findings_to_export)} findings will be included in the report.")
    else:
        st.info(f"🧾 Exporting all {len(findings_to_export)} findings.")

    # 🧩 Export preview table
    if findings_to_export:
        import pandas as pd
        preview_data = [
            {
                "ID": f.get("id", ""),
                "Title": f.get("title", ""),
                "Severity": f.get("severity", ""),
                "CVSS": f.get("cvss", ""),
                "Recommendation": (f.get("recommendation", "")[:100] + "...") if len(f.get("recommendation", "")) > 100 else f.get("recommendation", "")
            }
            for f in findings_to_export
        ]
        df_preview = pd.DataFrame(preview_data)
        st.markdown("### 🔍 Export Preview")
        st.dataframe(df_preview, width="stretch")
    else:
        st.warning("⚠️ No findings selected for export.")

    # Prepare modified report object for export
    export_report = r.copy()
    export_report["findings"] = findings_to_export

    # Export buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📄 Generate PDF Report"):
            pdf_bytes = generate_pdf_bytes(export_report, watermark="CONFIDENTIAL" if add_wm else None)
            st.download_button(
                "⬇️ Download PDF",
                data=pdf_bytes,
                file_name=f"report_{export_report.get('client','')}.pdf",
                mime="application/pdf"
            )
            b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

    with c2:
        if st.button("📝 Generate DOCX Report"):
            docx_bytes = generate_docx_bytes(export_report, watermark="CONFIDENTIAL" if add_wm else None)
            st.download_button(
                "⬇️ Download DOCX",
                data=docx_bytes,
                file_name=f"report_{export_report.get('client','')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
