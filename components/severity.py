# components/severity.py
import streamlit as st

def render():
    st.subheader("Finding Severity Ratings")

    text = st.text_area(
        "Edit Severity Rating Definitions",
        value=getattr(st.session_state, 'severity_ratings',
            "Critical: 9.0 - 10.0\n"
            "High: 7.0 - 8.9\n"
            "Medium: 4.0 - 6.9\n"
            "Low: 0.1 - 3.9"),
        height=150,
        key="severity_input"
    )
    if text != st.session_state.get('severity_ratings'):
        st.session_state.severity_ratings = text
