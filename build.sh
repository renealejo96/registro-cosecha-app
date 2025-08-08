#!/bin/bash
echo "🔧 Configurando build para Render..."

# Actualizar pip y setuptools
python -m pip install --upgrade pip setuptools wheel

# Instalar dependencias con configuraciones optimizadas
pip install --no-cache-dir --prefer-binary -r requirements.txt

echo "✅ Build completado exitosamente"
