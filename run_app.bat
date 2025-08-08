@echo off
echo Iniciando aplicacion de Registro de Cosecha...
echo.
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
pause
