#!/bin/bash
echo "Instalare dependențe..."
python3 -m pip install -r requirements.txt

echo "Pornire raport..."
python3 -m streamlit run main.py --server.port=8501
