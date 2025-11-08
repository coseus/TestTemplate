# parsers/nmap.py
import re

def parse_nmap(file_content):
    findings = []
    try:
        text = file_content.decode('utf-8', errors='ignore')
        lines = text.splitlines()
        current_host = None
        for line in lines:
            if line.startswith("Nmap scan report for"):
                current_host = line.split("for", 1)[1].strip()
            elif re.match(r"^\d+/(tcp|udp)\s+open", line):
                parts = line.split()
                port_proto = parts[0]
                service = parts[2] if len(parts) > 2 else "unknown"
                findings.append({
                    "id": f"{current_host}-{port_proto}",
                    "title": f"Open port: {port_proto} ({service}) on {current_host}",
                    "severity": "Informational",
                    "cvss": "N/A",
                    "description": f"Port {port_proto} is open and running {service}.",
                    "impact": "Potential attack surface.",
                    "recommendation": "Ensure only required services are exposed.",
                    "code": "",
                    "images": []
                })
    except Exception as e:
        raise ValueError(f"Error parsing Nmap: {e}")
    return findings
