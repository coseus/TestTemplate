# report/sections/executive.py
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors
from reportlab.lib.units import inch
import streamlit as st
import pandas as pd
import plotly.express as px

# === PENTRU PDF ===
def add_executive_summary(pdf, findings, executive_text="", **kwargs):
    pdf.story.append(Paragraph("Executive Summary", pdf.styles['Heading1']))
    pdf.story.append(Spacer(1, 12))

    # PIE CHART
    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = [sum(1 for f in findings if f.get("severity") == sev) for sev in levels]

    d = Drawing(400, 220)
    pc = Pie()
    pc.x = 120; pc.y = 20; pc.width = pc.height = 150
    pc.data = counts
    pc.labels = levels
    pc.slices.strokeWidth = 0.5
    pc.slices[0].fillColor = colors.HexColor("#dc2626")
    pc.slices[1].fillColor = colors.HexColor("#f97316")
    pc.slices[2].fillColor = colors.HexColor("#facc15")
    pc.slices[3].fillColor = colors.HexColor("#10b981")
    pc.slices[4].fillColor = colors.HexColor("#6366f1")
    d.add(pc)
    pdf.story.append(d)
    pdf.story.append(Spacer(1, 20))

    # TABEL SUB GRAFIC
    data = [["Severity", "Count"]] + [[sev, str(counts[i])] for i, sev in enumerate(levels)]
    table = Table(data, colWidths=[3*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 12),
    ]))
    pdf.story.append(table)
    pdf.story.append(Spacer(1, 20))

    # TEXT DIN UI
    if executive_text:
        for para in [p.strip() for p in executive_text.split("\n") if p.strip()]:
            pdf.story.append(Paragraph(para, pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.1 * inch))

    # FĂRĂ PageBreak() → se adaugă în generator.py
# === PENTRU WEB (Streamlit) ===
def render():
    st.subheader("Executive Summary")

    if not st.session_state.get("findings"):
        st.info("No findings yet.")
        return

    # PIE CHART INTERACTIV
    levels = ["Critical", "High", "Moderate", "Low", "Informational"]
    counts = {sev: sum(1 for f in st.session_state.findings if f.get("severity") == sev) for sev in levels}
    df = pd.DataFrame(list(counts.items()), columns=["Severity", "Count"])

    fig = px.pie(
        df, values="Count", names="Severity",
        color_discrete_sequence=["#dc2626", "#f97316", "#facc15", "#10b981", "#6366f1"],
        hole=0.4
    )
    fig.update_layout(title="Vulnerability Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # TABEL
    st.markdown("#### Severity Breakdown")
    st.table(df)

    # TEXT AREA
    current_text = st.session_state.get("executive_summary_text", "")
    new_text = st.text_area(
        "Executive Summary Text",
        value=current_text,
        height=150,
        key="exec_summary_text_area"
    )
    if st.button("Save Text", key="save_exec_text"):
        st.session_state.executive_summary_text = new_text
        st.success("Executive Summary saved!")
