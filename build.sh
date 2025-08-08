#!/bin/bash
set -e  # Salir si hay errores

echo "🔧 Iniciando build optimizado para Render..."

# Actualizar setuptools y pip primero
echo "📦 Actualizando herramientas de build..."
python -m pip install --upgrade pip>=22.0.0
python -m pip install --upgrade setuptools>=65.0.0 wheel>=0.38.0

# Limpiar cache
echo "🧹 Limpiando cache..."
python -m pip cache purge

# Instalar dependencias con configuraciones optimizadas
echo "📚 Instalando dependencias..."
python -m pip install --no-cache-dir --prefer-binary --timeout 1000 -r requirements.txt

echo "✅ Build completado exitosamente"
