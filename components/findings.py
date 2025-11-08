# components/findings.py
import streamlit as st
import xml.etree.ElementTree as ET
import base64
from collections import Counter

def render():
    st.subheader("Technical Findings")

    # === CONTOR LIVE ===
    total = len(st.session_state.findings)
    sev_count = Counter(f.get("severity", "Unknown") for f in st.session_state.findings)
    st.markdown(
        f"**Total Findings: {total}** | "
        f"Critical: {sev_count['Critical']} | "
        f"High: {sev_count['High']} | "
        f"Moderate: {sev_count['Moderate']} | "
        f"Low: {sev_count['Low']} | "
        f"Informational: {sev_count['Informational']}"
    )

    # === TABURI ===
    tab1, tab2 = st.tabs(["Add / Edit Manual", "Import Nessus / Nmap"])

    # ===================================================================
    # TAB 1: ADD MANUAL + EDIT + DELETE
    # ===================================================================
    with tab1:
        with st.expander("Add New Finding", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                fid = st.text_input("ID", "VULN-001", key="add_id")
                title = st.text_input("Title", key="add_title")
                host = st.text_input("Host / IP", "192.168.1.10", key="add_host")
            with col2:
                severity = st.selectbox(
                    "Severity",
                    ["Critical", "High", "Moderate", "Low", "Informational"],
                    key="add_sev"
                )
                cvss = st.number_input("CVSS Score", 0.0, 10.0, 0.0, 0.1, key="add_cvss")

            description = st.text_area("Description", height=100, key="add_desc")
            remediation = st.text_area("Remediation", height=100, key="add_rem")
            code = st.text_area("Proof of Concept (Code)", height=120, key="add_code", placeholder="curl -X POST ...")

            uploaded_images = st.file_uploader(
                "Upload Screenshots (PNG/JPG)",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="add_images"
            )
            images_b64 = [f"data:{img.type};base64,{base64.b64encode(img.read()).decode()}" for img in uploaded_images]

            if st.button("Add Finding", type="primary"):
                st.session_state.findings.append({
                    "id": fid,
                    "title": title,
                    "host": host,
                    "severity": severity,
                    "cvss": cvss,
                    "description": description,
                    "remediation": remediation,
                    "code": code,
                    "images": images_b64
                })
                st.success("Finding added!")
                st.rerun()

        # === LISTĂ FINDINGS ===
        if st.session_state.findings:
            for i, f in enumerate(st.session_state.findings):
                with st.expander(f"**{f.get('id')}** - {f.get('title')} | {f.get('host')} | {f.get('severity')}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        with st.form(key=f"edit_form_{i}"):
                            e_id = st.text_input("ID", f.get("id"), key=f"e_id_{i}")
                            e_title = st.text_input("Title", f.get("title"), key=f"e_title_{i}")
                            e_host = st.text_input("Host", f.get("host"), key=f"e_host_{i}")
                            e_sev = st.selectbox("Severity", ["Critical", "High", "Moderate", "Low", "Informational"],
                                                index=["Critical", "High", "Moderate", "Low", "Informational"].index(f.get("severity", "Moderate")),
                                                key=f"e_sev_{i}")
                            e_cvss = st.number_input("CVSS", 0.0, 10.0, float(f.get("cvss", 0)), 0.1, key=f"e_cvss_{i}")
                            e_desc = st.text_area("Description", f.get("description", ""), height=100, key=f"e_desc_{i}")
                            e_rem = st.text_area("Remediation", f.get("remediation", ""), height=100, key=f"e_rem_{i}")
                            e_code = st.text_area("Code", f.get("code", ""), height=120, key=f"e_code_{i}")

                            uploaded_edit = st.file_uploader("Replace images", type=["png","jpg","jpeg"], accept_multiple_files=True, key=f"edit_imgs_{i}")
                            new_images = [f"data:{img.type};base64,{base64.b64encode(img.read()).decode()}" for img in uploaded_edit]
                            current_images = new_images or f.get("images", [])

                            if st.form_submit_button("Save"):
                                st.session_state.findings[i] = {
                                    "id": e_id, "title": e_title, "host": e_host, "severity": e_sev,
                                    "cvss": e_cvss, "description": e_desc, "remediation": e_rem,
                                    "code": e_code, "images": current_images
                                }
                                st.success("Updated!")
                                st.rerun()

                    with col2:
                        if st.button("Delete", key=f"del_{f.get('id')}_{i}"):
                            st.session_state.findings.pop(i)
                            st.success("Deleted!")
                            st.rerun()

                    if f.get("images"):
                        cols = st.columns(3)
                        for idx, img in enumerate(f["images"]):
                            with cols[idx % 3]:
                                st.image(img, use_column_width=True)
        else:
            st.info("No findings yet.")

    # ===================================================================
    # TAB 2: IMPORT NESSUS / NMAP
    # ===================================================================
    with tab2:
        st.markdown("### Import Nessus (.nessus) or Nmap (.xml)")
        uploaded_file = st.file_uploader("Upload file", type=["nessus", "xml"], key="import_uploader")

        if uploaded_file:
            min_severity = st.selectbox(
                "Minimum Severity to Import",
                ["Informational", "Low", "Moderate", "High", "Critical"],
                index=2
            )
            sev_map = {"Informational": 0, "Low": 1, "Moderate": 2, "High": 3, "Critical": 4}
            min_val = sev_map[min_severity]

            if st.button("Import Selected", type="primary"):
                try:
                    file_ext = uploaded_file.name.split(".")[-1].lower()
                    tree = ET.parse(uploaded_file)
                    root = tree.getroot()
                    imported = 0

                    if file_ext == "nessus":
                        # Nessus v2 XML structure
                        for report_host in root.findall(".//ReportHost"):
                            host = report_host.get("name")
                            for item in report_host.findall("ReportItem"):
                                sev = int(item.get("severity", "0"))
                                if sev < min_val:
                                    continue

                                plugin_id = item.get("pluginID")
                                plugin_name = item.find("plugin_name")
                                plugin_name = plugin_name.text if plugin_name is not None else "Unknown"

                                desc = item.find("description")
                                sol = item.find("solution")
                                cvss_elem = item.find("cvss3_base_score")

                                st.session_state.findings.append({
                                    "id": f"NESSUS-{plugin_id}",
                                    "title": plugin_name,
                                    "host": host,
                                    "severity": {0: "Informational", 1: "Low", 2: "Moderate", 3: "High", 4: "Critical"}.get(sev, "Unknown"),
                                    "cvss": float(cvss_elem.text) if cvss_elem is not None and cvss_elem.text else 0.0,
                                    "description": (desc.text[:500] + "...") if desc is not None and desc.text else "",
                                    "remediation": sol.text if sol is not None and sol.text else "",
                                    "code": "",
                                    "images": []
                                })
                                imported += 1

                    elif file_ext == "xml":
                        # Nmap
                        for host in root.findall(".//host"):
                            addr = host.find("address").get("addr")
                            for port in host.findall(".//port"):
                                if port.find("state").get("state") == "open":
                                    portid = port.get("portid")
                                    service = port.find("service")
                                    svc_name = service.get("name", "unknown") if service is not None else "unknown"
                                    st.session_state.findings.append({
                                        "id": f"NMAP-{addr}:{portid}",
                                        "title": f"Open Port {portid} ({svc_name})",
                                        "host": addr,
                                        "severity": "Informational",
                                        "cvss": 0.0,
                                        "description": f"Port {portid} open on {addr}",
                                        "remediation": "Close if not required",
                                        "code": "",
                                        "images": []
                                    })
                                    imported += 1

                    st.success(f"Imported **{imported}** findings!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Import failed: {e}")
                    st.code(str(e)[:1000])
