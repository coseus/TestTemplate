# parsers/__init__.py
from .nessus import parse_nessus
from .nmap import parse_nmap  # ← FUNCȚIE

__all__ = ['parse_nessus', 'parse_nmap']
