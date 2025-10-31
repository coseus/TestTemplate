pentest_report - modular pentest report generator

Structure:
- app.py : Streamlit front-end (minimal)
- report/ : package with modules:
    - data_model.py
    - utils.py
    - parsers.py
    - numbering.py
    - pdf_generator.py
    - docx_generator.py

Usage:
1. pip install -r requirements.txt
2. streamlit run app.py
