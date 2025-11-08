# components/legal.py
import streamlit as st

def render():
    st.subheader("Legal Statements")

    # Confidentiality
    with st.expander("Confidentiality Statement", expanded=True):
        text = st.text_area(
            "Edit Confidentiality Statement",
            value=getattr(st.session_state, 'confidentiality', 
                "This report contains sensitive information and is intended solely for the use of the named client.\n"
                "Unauthorized distribution, copying, or disclosure is strictly prohibited."),
            height=120,
            key="confidentiality_input"
        )
        if text != st.session_state.get('confidentiality'):
            st.session_state.confidentiality = text

    # Disclaimer
    with st.expander("Disclaimer", expanded=True):
        text = st.text_area(
            "Edit Disclaimer",
            value=getattr(st.session_state, 'disclaimer',
                "The results presented reflect the state of the systems at the time of testing.\n"
                "No implicit or explicit guarantees are provided regarding future security.\n"
                "Responsibility for implementing recommendations lies with the client."),
            height=120,
            key="disclaimer_input"
        )
        if text != st.session_state.get('disclaimer'):
            st.session_state.disclaimer = text
