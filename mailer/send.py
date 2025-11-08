# mailer/send.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

# DEBUG SMTP
logging.basicConfig(level=logging.DEBUG)

def send_report(
    email_to, project_name, pdf_path, docx_path=None,
    smtp_server="smtp.gmail.com", smtp_port=587, use_tls=True,
    email_user=None, email_pass=None
):
    if not email_user or not email_pass:
        return False, "Email și App Password necesare!"

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = f"Pentest Report - {project_name}"

    body = f"""
    <h3>Raport de Securitate</h3>
    <p>Atașat găsești raportul pentru <b>{project_name}</b>.</p>
    <p>Cu stimă,<br/>Echipa de Securitate</p>
    """
    msg.attach(MIMEText(body, 'html'))

    # === ATAȘEAZĂ PDF ===
    if not os.path.exists(pdf_path):
        return False, "PDF nu există!"
    with open(pdf_path, "rb") as f:
        attach = MIMEBase('application', 'pdf')
        attach.set_payload(f.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment; filename=report.pdf')
        msg.attach(attach)

    # === ATAȘEAZĂ DOCX ===
    if docx_path and os.path.exists(docx_path):
        with open(docx_path, "rb") as f:
            attach = MIMEBase('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document')
            attach.set_payload(f.read())
            encoders.encode_base64(attach)
            attach.add_header('Content-Disposition', 'attachment; filename=report.docx')
            msg.attach(attach)

    # === CONECTARE SMTP – FIXAT PENTRU GMAIL & YAHOO ===
    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            server.ehlo()  # ← NECESAR PENTRU GMAIL/YAHOO
            if use_tls:
                server.starttls()
                server.ehlo()  # ← DIN NOU DUPĂ STARTTLS

        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True, "Email trimis cu succes!"

    except smtplib.SMTPAuthenticationError as e:
        return False, "Autentificare eșuată: Verifică App Password!"
    except smtplib.SMTPServerDisconnected:
        return False, "Server deconectat. Încearcă din nou."
    except Exception as e:
        return False, f"Eroare SMTP: {str(e)}"
