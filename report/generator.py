# report/generator.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, PageBreak, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import os
from reportlab.pdfgen import canvas

# Import secțiuni
from .sections.cover import add_cover
from .sections.toc import add_toc
from .sections.legal import add_legal
from report.sections.contact import add_contact_section
from .sections.overview import add_overview
from .sections.scope import add_scope
from .sections.severity import add_severity_ratings
from .sections.executive import add_executive_summary
from .sections.findings import add_technical_findings
from .sections.poc import add_poc

# === IMPORT CONFIG ===
from config import TITLE_COLOR, COVER_TITLE_COLOR, PAGE_HEADER_LOGO

class PDFReport:
    def __init__(self, logo_path=None, watermark=False, title_color=None, cover_color=None):
        self.buffer = BytesIO()
        self.logo_path = logo_path or PAGE_HEADER_LOGO
        self.watermark = watermark
        # === CULOARE DINAMICĂ (din UI sau config) ===
        self.title_color = colors.HexColor(title_color or TITLE_COLOR)
        self.cover_color = colors.HexColor(cover_color or COVER_TITLE_COLOR)
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            topMargin=1.2 * inch,
            bottomMargin=0.8 * inch,
            leftMargin=0.7 * inch,
            rightMargin=0.7 * inch
        )
        self.styles = self._create_styles()
        self.story = []

# report/generator.py → în def _create_styles(self):

    def _create_styles(self):
        styles = getSampleStyleSheet()
    
        # === TITLU SECȚIUNI (dinamic) ===
        styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=styles['Heading2'],
            textColor=self.title_color,
            fontSize=14,
            leading=18,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
    
        # === COVER TITLE (dinamic) ===
        styles.add(ParagraphStyle(
            name='CoverTitle',
            fontSize=28,
            leading=32,
            alignment=1,
            textColor=self.cover_color,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        ))
    
        # === CONFIDENTIAL (pentru cover) ===
        styles.add(ParagraphStyle(
            name='Confidential',
            fontSize=36,
            textColor=colors.HexColor("#CCCCCC"),
            alignment=1,
            fontName='Helvetica-Bold',
            spaceAfter=0
        ))
    
        # === WATERMARK (dacă e activat) ===
        styles.add(ParagraphStyle(
            name='Watermark',
            fontSize=60,
            textColor=colors.HexColor("#CCCCCC"),
            alignment=1,
            spaceAfter=0,
            fontName='Helvetica'
        ))
    
        return styles

    def _header(self, canvas, doc):
        if self.logo_path and os.path.exists(self.logo_path):
            canvas.saveState()
            logo = Image(self.logo_path, width=1.2*inch, height=0.6*inch)
            logo.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 0.8*inch)
            canvas.restoreState()

        # Linie sub logo
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#003366"))
        canvas.setLineWidth(2)
        canvas.line(doc.leftMargin, doc.height + doc.topMargin - 0.9*inch,
                    doc.width + doc.leftMargin, doc.height + doc.topMargin - 0.9*inch)
        canvas.restoreState()

        # Page number
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(
            doc.leftMargin + doc.width / 2,
            doc.bottomMargin - 0.3 * inch,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    def generate(self, findings, client, project, executive_text=None,
                 tester=None, date=None, scope=None, overview_text=None,
                 poc_list=None, **kwargs):
        poc_list = poc_list or []
        findings = findings or []

        # === SECȚIUNI ===
        add_cover(self, client=client, project=project, tester=tester, date=date)
        self.story.append(PageBreak())

        add_toc(self, findings=findings, poc_list=poc_list)
        self.story.append(PageBreak())

        add_legal(self, client=client)
        add_contact_section(self)
        self.story.append(PageBreak())

        add_overview(self, overview_text=overview_text)
        add_scope(self, scope=scope)
        add_severity_ratings(self)
        self.story.append(PageBreak())

        add_executive_summary(self, findings=findings, executive_text=executive_text)
        self.story.append(PageBreak())

        add_technical_findings(self, findings=findings)
        self.story.append(PageBreak())

        add_poc(self, poc_list=poc_list)

        # === BUILD PDF ===
        self.doc.build(
            self.story,
            onFirstPage=self._header,
            onLaterPages=self._header
        )
        return self.buffer.getvalue()
