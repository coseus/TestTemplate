# report/sections/__init__.py
from .cover import add_cover
from .toc import add_toc
from .legal import add_legal
from .contact import add_contact_section
from .overview import add_overview
from .scope import add_scope
from .severity import add_severity_ratings
from .summary import add_vulnerability_summary
from .executive import add_executive_summary
from .findings import add_technical_findings
from .poc import add_poc

__all__ = [
    'add_cover', 'add_toc', 'add_legal', 'add _contact',
    'add_assessment_overview', 'add_scope', 'add_severity_ratings',
    'add_vulnerability_summary', 'add_executive_summary',
    'add_technical_findings', 'add_poc'
]
