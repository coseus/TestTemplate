@echo off
echo Instalare dependențe...
pip install -r requirements.txt

echo Pornire raport...
streamlit run app.py --server.port=8501
pause
