# parsers/nessus.py
import xml.etree.ElementTree as ET

def parse_nessus(file_content):
    findings = []
    try:
        # Nessus poate avea BOM sau caractere ciudate → curăță
        content_str = file_content.decode('utf-8', errors='ignore')
        root = ET.fromstring(content_str)

        # Suportă ambele formate: <NessusClientData_v2> și <report>
        report_hosts = root.findall(".//ReportHost") or root.findall(".//host")

        for report_host in report_hosts:
            host = report_host.get("name") or report_host.findtext("host-ip") or "Unknown"
            items = report_host.findall("ReportItem") or report_host.findall("vuln")

            for item in items:
                plugin_name = (
                    item.get("pluginName") or
                    item.get("plugin_name") or
                    item.findtext("name") or
                    "Unknown Vulnerability"
                )
                severity_num = item.get("severity", "0")
                sev_map = {"0": "Informational", "1": "Low", "2": "Moderate", "3": "High", "4": "Critical"}
                severity = sev_map.get(severity_num, "Informational")

                description = _get_text(item, ["description", "plugin_output", "synopsis"])
                risk_factor = _get_text(item, ["risk_factor", "plugin_output"])
                solution = _get_text(item, ["solution", "see_also"])

                cvss = (
                    item.findtext("cvss3_base_score") or
                    item.findtext("cvss_base_score") or
                    "N/A"
                )

                plugin_id = item.get("pluginID") or item.get("id") or "N/A"

                findings.append({
                    "id": f"{host}-{plugin_id}",
                    "title": f"[{host}] {plugin_name}",
                    "severity": severity,
                    "cvss": cvss,
                    "description": description or "N/A",
                    "impact": risk_factor or "N/A",
                    "recommendation": solution or "N/A",
                    "code": "",
                    "images": []
                })
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML in Nessus file: {e}")
    except Exception as e:
        raise ValueError(f"Error parsing Nessus: {e}")
    return findings

def _get_text(element, tags):
    for tag in tags:
        el = element.find(tag)
        if el is not None and el.text:
            return el.text.strip()
    return None
