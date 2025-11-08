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
#from .sections.contact import add_contact
from report.sections.contact import add_contact_section
from .sections.overview import add_overview
from .sections.scope import add_scope
from .sections.severity import add_severity_ratings
from .sections.executive import add_executive_summary
from .sections.findings import add_technical_findings
from .sections.poc import add_poc
from config import TITLE_COLOR, COVER_TITLE_COLOR, WATERMARK_TEXT, WATERMARK_COLOR, WATERMARK_FONTSIZE, WATERMARK_ANGLE

class PDFReport:
    def __init__(self, logo_path=None, watermark=False, title_color=None, cover_color=None):
        self.buffer = BytesIO()
        self.logo_path = logo_path or PAGE_HEADER_LOGO
        self.watermark = watermark
        self.title_color = colors.HexColor(title_color or TITLE_COLOR)
        self.cover_color = colors.HexColor(cover_color or COVER_TITLE_COLOR)
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            topMargin=1.2 * inch,      # Spațiu pentru header (logo + linie)
            bottomMargin=0.8 * inch,
            leftMargin=0.7 * inch,
            rightMargin=0.7 * inch
        )
        self.styles = self._create_styles()
        self.story = []

    def _create_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CorporateTitle',
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#003366")
        ))
        styles.add(ParagraphStyle(
            name='CorporateSubtitle',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555")
        ))
        styles.add(ParagraphStyle(
            name='Confidential',
            fontSize=10,
            textColor=colors.red,
            alignment=TA_CENTER
        ))
        return styles

    def _header(self, canvas, doc):
        """Logo + linie subțire – pe toate paginile"""
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image(self.logo_path, width=1.3 * inch, height=0.65 * inch)
                logo.drawOn(canvas, 0.7 * inch, doc.height + 1.0 * inch)
            except Exception:
                print(f"Logo error: {e}")

        # Linie sub logo
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#003366"))
        canvas.setLineWidth(1)
        canvas.line(
            0.7 * inch,
            doc.height + 0.9 * inch,
            doc.width + 0.7 * inch,
            doc.height + 0.9 * inch
        )
        canvas.restoreState()
        if self.watermark:
            canvas.saveState()
            canvas.setFont("Helvetica-Bold", 72)
            canvas.setFillColor(colors.HexColor("#e5e7eb"), 0.15)  # 15% opacitate
            canvas.translate(doc.width/2 + doc.leftMargin, doc.height/2 + doc.bottomMargin)
            canvas.rotate(45)
            canvas.drawCentredString(0, 0, "CONFIDENTIAL")
            canvas.restoreState()

        # === NUMĂR PAGINĂ (NU PE COVER) ===
        if doc.page > 1:  # ← FĂRĂ PE PAGINA 1
            canvas.saveState()
            canvas.setFont("Helvetica", 10)
            canvas.setFillColor(colors.HexColor("#003366"))
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

        # PAGINA 1 – COVER
        add_cover(self, client=client, project=project, tester=tester, date=date)
       # self.story.append(PageBreak())

        # PAGINA 2 – TOC
       	add_toc(self, findings=findings, poc_list=poc_list)
       	self.story.append(PageBreak())

        # PAGINA 3 – LEGAL + CONTACT
        add_legal(self, client=client)
       #add_contact(self, client=client, tester=tester)
        add_contact_section(self)
        self.story.append(PageBreak())

        # PAGINA 4 – OVERVIEW + SCOPE + SEVERITY
        add_overview(self, overview_text=overview_text)
        add_scope(self, scope=scope)
        add_severity_ratings(self, **kwargs)
        self.story.append(PageBreak())

        # PAGINA 5 – EXECUTIVE
        add_executive_summary(self, findings=findings, executive_text=executive_text)
        self.story.append(PageBreak())

        # PAGINA 6+ – FINDINGS
        add_technical_findings(self, findings=findings)
        self.story.append(PageBreak())

        # PAGINA 7+ – POC
        add_poc(self, poc_list=poc_list)


        # BUILD PDF CU HEADER PE TOATE PAGINILE
        self.doc.build(
            self.story,
            onFirstPage=self._header,
            onLaterPages=self._header
        )
        return self.buffer.getvalue()
