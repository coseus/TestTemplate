# report/sections/poc.py
from reportlab.platypus import Paragraph, Spacer, PageBreak, Image, KeepInFrame, Table
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage
import io
import base64

def add_poc(pdf, poc_list=None, **kwargs):
    poc_list = poc_list or []
    if not poc_list:
        pdf.story.append(Paragraph("No PoC entries.", pdf.styles['Normal']))
        pdf.story.append(PageBreak())
        return

    pdf.story.append(Paragraph("Steps to Reproduce", pdf.styles['SectionTitle']))
    pdf.story.append(Spacer(1, 0.2 * inch))

    for i, poc in enumerate(poc_list, 1):
        pdf.story.append(Paragraph(f"7.{i} {poc.get('title', 'PoC')}", pdf.styles['Heading2']))
        pdf.story.append(Spacer(1, 0.15 * inch))

        # Descriere
        if poc.get("description"):
            pdf.story.append(Paragraph(f"<b>Description:</b> {poc['description']}", pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.1 * inch))

        # Cod
        if poc.get("code"):
            safe_code = poc["code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            code_block = f"<pre><font name='Courier'>{safe_code}</font></pre>"
            pdf.story.append(Paragraph(code_block, pdf.styles['Normal']))
            pdf.story.append(Spacer(1, 0.1 * inch))

        # === IMAGINI (base64 strings) ===
        for img_b64 in poc.get("images", []):
            if not img_b64 or not isinstance(img_b64, str) or not img_b64.startswith("data:image"):
                continue
            try:
                header, b64_data = img_b64.split(",", 1)
                img_bytes = base64.b64decode(b64_data)
                pil_img = PILImage.open(io.BytesIO(img_bytes)).convert("RGB")

                buffer = io.BytesIO()
                pil_img.save(buffer, format="JPEG", quality=85)
                buffer.seek(0)

                img = Image(buffer, width=6*inch, height=3.5*inch)
                img.hAlign = TA_CENTER
                framed = KeepInFrame(maxWidth=6*inch, maxHeight=4*inch, content=[img])
                pdf.story.append(framed)
                pdf.story.append(Spacer(1, 0.1 * inch))

            except Exception as e:
                pdf.story.append(Paragraph(f"[Image error: {e}]", pdf.styles['Normal']))

        pdf.story.append(Spacer(1, 0.3 * inch))

    pdf.story.append(PageBreak())
