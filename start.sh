#!/bin/bash
# Script de inicio para Render
echo "Iniciando aplicación de Registro de Cosecha..."
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.fileWatcherType none
