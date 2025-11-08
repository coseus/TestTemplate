# components/overview.py
import streamlit as st

def render():
    st.subheader("Assessment Overview")
    overview_text = st.text_area(
        "Write your assessment overview here...",
        height=200,
        key="overview_text_input"
    )
    if st.button("Save Overview", key="save_overview_btn"):
        st.session_state.overview_text = overview_text
        st.success("Overview saved!")
