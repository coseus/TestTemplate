# report/sections/executive.py
from reportlab.platypus import Paragraph, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
import streamlit as st
import pandas as pd
import plotly.express as px

# report/sections/summary.py
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch

def add_vulnerability_summary(report, findings):
    report.story.append(Paragraph("Vulnerability Summary", report.styles['Heading1']))
    report.story.append(Spacer(1, 12))

    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = {sev: sum(1 for f in findings if f["severity"] == sev) for sev in levels}

    data = [["Severity", "Count"]] + [[sev, str(counts[sev])] for sev in levels]
    table = Table(data, colWidths=[3*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 12),
    ]))
    report.story.append(table)

# === PENTRU PDF ===
def add_executive_summary(report, findings, **kwargs):
    report.story.append(Paragraph("Executive Summary", report.styles['Heading1']))
    report.story.append(Spacer(1, 12))

    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = [sum(1 for f in findings if f["severity"] == sev) for sev in levels]

    d = Drawing(400, 220)
    pc = Pie()
    pc.x = 120
    pc.y = 20
    pc.width = pc.height = 150
    pc.data = counts
    pc.labels = levels
    pc.slices.strokeWidth = 0.5
    pc.slices[0].fillColor = HexColor("#dc2626")
    pc.slices[1].fillColor = HexColor("#f97316")
    pc.slices[2].fillColor = HexColor("#facc15")
    pc.slices[3].fillColor = HexColor("#10b981")
    pc.slices[4].fillColor = HexColor("#6366f1")
    d.add(pc)
    report.story.append(d)

    report.story.append(Spacer(1, 12))
    report.story.append(Paragraph("Key risks have been identified and prioritized.", report.styles['Normal']))

# === PENTRU WEB (Streamlit) ===
def render():
    st.subheader("Executive Summary")
    if not st.session_state.get("findings"):
        st.info("No findings yet.")
        return

    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = {sev: sum(1 for f in st.session_state.findings if f["severity"] == sev) for sev in levels}
    df = pd.DataFrame(list(counts.items()), columns=["Severity", "Count"])

    fig = px.pie(df, values="Count", names="Severity", 
                 color_discrete_sequence=["#dc2626", "#f97316", "#facc15", "#10b981", "#6366f1"],
                 hole=0.4)
    fig.update_layout(title="Vulnerability Distribution", legend_title="Severity")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Key Insights:**")
    st.markdown("- Immediate action required for **Critical** issues.")
    st.markdown("- Patch **High** risk within 7 days.")
