# components/general.py
import streamlit as st
from datetime import date

def render():
    st.subheader("General Information")

    # === PREIA DATE DIN session_state ===
    client = st.session_state.get("client", "")
    project = st.session_state.get("project", "")
    tester = st.session_state.get("tester", "")
    saved_date = st.session_state.get("date")

    # === CONVERTEȘTE DATA ===
    try:
        if saved_date and isinstance(saved_date, str):
            from datetime import datetime
            initial_date = datetime.strptime(saved_date, "%Y-%m-%d").date()
        else:
            initial_date = saved_date or date.today()
    except:
        initial_date = date.today()

    # === FORMULAR GENERAL ===
    col1, col2 = st.columns(2)
    with col1:
        client_input = st.text_input("Client Name", value=client, key="client_input")
        project_input = st.text_input("Project Name", value=project, key="project_input")
    with col2:
        tester_input = st.text_input("Tester", value=tester, key="tester_input")
        report_date = st.date_input("Report Date", value=initial_date, key="date_input")

    # === SAVE GENERAL INFO ===
    if st.button("Save General Info", type="primary"):
        st.session_state.client = client_input
        st.session_state.project = project_input
        st.session_state.tester = tester_input
        st.session_state.date = report_date
        st.success("General info saved!")
        st.rerun()

    # ========================================
    # === ASSESSMENT OVERVIEW (REAPARE) ===
    # ========================================
    st.markdown("---")
    st.subheader("Assessment Overview")

    overview_text = st.text_area(
        "Write your assessment overview here...",
        value=st.session_state.get("overview_text", ""),
        height=200,
        key="overview_text_area"
    )

    if st.button("Save Overview", type="secondary"):
        st.session_state.overview_text = overview_text
        st.success("Assessment Overview saved!")
        st.rerun()

    # ========================================
    # === CONTACT INFORMATION (DINAMIC) ===
    # ========================================
    st.markdown("---")
    st.subheader("Contact Information")

    # Inițializează lista
    if "contacts" not in st.session_state:
        st.session_state.contacts = [
            {"name": "Cosmin Ivascu", "role": "Lead Security Analyst", "email": "security@company.com", "type": "Tester"},
            {"name": "Electrogrup S.A", "role": "Client Representative", "email": "client@company.com", "type": "Client"},
            {"name": "Support", "role": "Support Team", "email": "support@company.com", "type": "Support"}
        ]

    # === ADAUGĂ CONTACT ===
    with st.expander("Add New Contact", expanded=False):
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        with col1:
            new_name = st.text_input("Name", key="new_contact_name")
        with col2:
            new_role = st.text_input("Role", key="new_contact_role")
        with col3:
            new_email = st.text_input("Email", key="new_contact_email")
        with col4:
            new_type = st.selectbox("Type", ["Tester", "Client", "Support", "Other"], key="new_contact_type")

        if st.button("Add Contact", type="primary"):
            if new_name and new_email:
                st.session_state.contacts.append({
                    "name": new_name,
                    "role": new_role,
                    "email": new_email,
                    "type": new_type
                })
                st.success("Contact added!")
                st.rerun()
            else:
                st.error("Name and Email required!")

    # === TABEL LIVE + DELETE ===
    st.markdown("### Current Contacts")
    if st.session_state.contacts:
        cols = st.columns([3, 3, 3, 2, 1])
        headers = ["Name", "Role", "Email", "Type", "Action"]
        for col, h in zip(cols, headers):
            col.markdown(f"**{h}**")

        st.markdown("---")

        for i, contact in enumerate(st.session_state.contacts):
            cols = st.columns([3, 3, 3, 2, 1])
            with cols[0]: st.write(contact["name"])
            with cols[1]: st.write(contact["role"])
            with cols[2]: st.write(contact["email"])
            with cols[3]: st.write(contact["type"])
            with cols[4]:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.contacts.pop(i)
                    st.success("Deleted!")
                    st.rerun()
    else:
        st.info("No contacts yet.")
