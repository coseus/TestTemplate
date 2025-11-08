# report/sections/scope.py
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle

def add_scope(report, **kwargs):
    scope_text = kwargs.get("scope", "No scope defined.")
    
    report.story.append(Paragraph("Scope of Testing", report.styles['SectionTitle']))
    report.story.append(Spacer(1, 12))
    
    lines = scope_text.split('\n')
    for line in lines:
        if line.strip().startswith("**") and line.strip().endswith("**"):
            text = line.replace("**", "")
            report.story.append(Paragraph(f"<b>{text}</b>", report.styles['Normal']))
        else:
            report.story.append(Paragraph(line, report.styles['Normal']))
