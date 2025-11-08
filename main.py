# main.py
# main.py
import streamlit as st
from components.general import render as general_tab
#from components.general import render_contacts
from components.scope import render as scope_tab
from components.findings import render as findings_tab
from components.exec_summary import render as exec_tab
from report.sections.executive import render as executive_summary
from components.poc import render as poc_tab
from components.export import render as export_tab  # ← FUNCȚIONAL
from components.legal import render as legal_tab
from components.severity import render as severity_tab

# ... restul codului rămâne la fel
st.set_page_config(page_title="Raport Pentest", layout="wide")
st.title("PENTEST REPORT GENERATOR")

# Inițializare
if 'findings' not in st.session_state:
    st.session_state.findings = []
if "poc_list" not in st.session_state:
    st.session_state.poc_list = []
if 'pocs' not in st.session_state:
    st.session_state.pocs = []
if 'poc_content' not in st.session_state:
    st.session_state.poc_content = ""
if 'overview' not in st.session_state:
    st.session_state.overview = ""
if 'confidentiality' not in st.session_state:
    st.session_state.confidentiality = ""
if 'disclaimer' not in st.session_state:
    st.session_state.disclaimer = ""
if 'severity_ratings' not in st.session_state:
    st.session_state.severity_ratings = ""

# Taburi
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "General Info", "Scope", "Findings", "Executive Summary", 
    "PoC", "Export"
])

with tab1: 
    general_tab()
#    render_contacts()
with tab2: scope_tab()
with tab3: findings_tab()
with tab4: executive_summary()
with tab5: poc_tab()
#with tab6: legal_tab()       # ← NOU
#with tab7: severity_tab()    # ← NOU
with tab6: export_tab()
