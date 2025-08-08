@echo off
echo ========================================
echo   PREPARANDO PROYECTO PARA DESPLIEGUE
echo ========================================
echo.

echo 1. Verificando Git...
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git no esta instalado. Descarga desde: https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo 2. Inicializando repositorio Git...
git init

echo.
echo 3. Agregando archivos...
git add .

echo.
echo 4. Creando primer commit...
git commit -m "Sistema de Registro de Cosecha - Version inicial"

echo.
echo 5. Configurando rama principal...
git branch -M main

echo.
echo ========================================
echo   LISTO PARA DESPLIEGUE!
echo ========================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Crear repositorio en GitHub:
echo    https://github.com/new
echo.
echo 2. Ejecutar estos comandos:
echo    git remote add origin https://github.com/TU_USUARIO/registro-cosecha.git
echo    git push -u origin main
echo.
echo 3. Desplegar en:
echo    - Streamlit Cloud: https://share.streamlit.io
echo    - Railway: https://railway.app
echo    - Render: https://render.com
echo.
echo ========================================
pause
