# config.py
# ==================================================
# CONFIGURAȚII GLOBALE – MODIFICĂ AICI, NU ÎN COD!
# ==================================================

# === CULORI PDF (titluri, cover, etc.) ===
TITLE_COLOR = "#003366"        # Toate titlurile secțiunilor
COVER_TITLE_COLOR = "#1e40af"  # Titlul de pe copertă
SEVERITY_COLORS = {
    "Critical": "#8B0000",
    "High": "#FF4500",
    "Moderate": "#FFD700",
    "Low": "#32CD32",
    "Informational": "#1E90FF"
}

# === EMAIL CONFIG (poți suprascrie în UI) ===
DEFAULT_SMTP = {
    "gmail": {
        "server": "smtp.gmail.com",
        "port": 587,
        "tls": True,
        "app_password_hint": "https://myaccount.google.com/apppasswords"
    },
    "yahoo": {
        "server": "smtp.mail.yahoo.com",
        "port": 587,
        "tls": True,
        "app_password_hint": "https://login.yahoo.com/myaccount/app-passwords"
    },
    "office365": {
        "server": "smtp.office365.com",
        "port": 587,
        "tls": True
    }
}

# === PDF STYLE ===
WATERMARK_TEXT = "CONFIDENTIAL"
WATERMARK_COLOR = "#CCCCCC"
WATERMARK_FONTSIZE = 60
WATERMARK_ANGLE = 30

PAGE_HEADER_LOGO = "assets/logo.png"  # Relativ la proiect
COVER_LOGO = "assets/cover_logo.png"

# === FONTURI (dacă vrei custom) ===
# FONT_NAME = "Helvetica"
# FONT_PATH = "assets/fonts/CustomFont.ttf"

# === TEXT DEFAULT (dacă nu e completat) ===
DEFAULT_CLIENT = "Client Name"
DEFAULT_PROJECT = "Penetration Test"
DEFAULT_TESTER = "Security Analyst"
DEFAULT_DATE = "November 2025"
