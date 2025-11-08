# report/utils/table.py
from reportlab.platypus import Table, TableStyle, Table
from reportlab.lib import colors
from reportlab.lib.units import inch

def add_table(pdf, data, col_widths, header_bg="#003366"):
    table = Table(data, colWidths=col_widths)
    style = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(header_bg)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]
    table.setStyle(TableStyle(style))
    pdf.story.append(table)
