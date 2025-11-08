# report/utils.py
def severity_color(sev):
    colors_map = {
        "Critical": "#dc2626",
        "High": "#f97316",
        "Moderate": "#facc15",
        "Low": "#10b981",
        "Informational": "#6366f1"
    }
    return colors_map.get(sev, "#000000")
