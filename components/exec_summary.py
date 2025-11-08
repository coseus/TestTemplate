# components/exec_summary.py
import streamlit as st
import plotly.graph_objects as go
from reportlab.lib.units import inch


def render():
    st.subheader("Executive Summary")
    
    text = st.text_area(
        "Summary for management",
        value=getattr(st.session_state, 'exec_summary', ''),
        height=200
    )
    if text != getattr(st.session_state, 'exec_summary', ''):
        st.session_state.exec_summary = text

    # Grafic live
    if st.session_state.findings:
        counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for f in st.session_state.findings:
            sev = f['severity']
            if sev == "Critică": counts["Critical"] += 1
            elif sev == "Înaltă": counts["High"] += 1
            elif sev == "Medie": counts["Medium"] += 1
            elif sev == "Joasă": counts["Low"] += 1
        labels = [f"{k} ({v})" for k, v in counts.items() if v > 0]
        values = [v for v in counts.values() if v > 0]
        colors = ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors)])
        fig.update_layout(title="Severity Distribution")
        st.plotly_chart(fig, width="stretch")
