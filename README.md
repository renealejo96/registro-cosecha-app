# 🌸 Aplicación de Registro de Cosecha

Una aplicación web desarrollada con Streamlit para registrar y visualizar datos de cosecha de flores.

## 🚀 Características

- ✅ Registro de cosecha por fecha, variedad y módulo
- 📊 Visualización gráfica de datos
- 📱 Interfaz optimizada para dispositivos móviles
- 📋 Tabla de registros guardados
- 🔢 Métricas de resumen

## 📦 Instalación Local

1. Asegúrate de tener Python 3.7+ instalado
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Ejecución Local

```bash
streamlit run app.py
```

## 🌐 Despliegue en Streamlit Cloud

### Pasos para desplegar:

1. **Ve a Streamlit Cloud:**
   ```
   https://share.streamlit.io
   ```

2. **Conecta con GitHub:**
   - Click "Sign up with GitHub"
   - Autoriza acceso a repositorios

3. **Deploy la aplicación:**
   ```
   Repository: renealejo96/registro-cosecha-app
   Branch: main
   Main file path: app.py
   ```

4. **¡Listo!**
   - Tu app estará disponible en una URL como:
   - `https://registro-cosecha-app-[hash].streamlit.app`

## 📱 Acceso desde Móvil

1. Abre el navegador en tu móvil
2. Ve a la URL de tu aplicación
3. Opcional: "Agregar a pantalla de inicio" para acceso rápido

## 📁 Estructura de Archivos

```
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── .streamlit/
│   └── config.toml       # Configuración del tema
└── data/
    ├── registros.csv     # Datos de registros
    ├── variedades.csv    # Lista de variedades
    └── modulos.csv       # Lista de módulos
```

## 🔧 Configuración

Los archivos CSV en la carpeta `data/` contienen:
- `variedades.csv`: Lista de variedades de flores disponibles
- `modulos.csv`: Lista de módulos/bloques de producción
- `registros.csv`: Datos de cosecha registrados (se genera automáticamente)

## 🎨 Personalización

Puedes modificar los colores y tema en `.streamlit/config.toml`

## 📞 Soporte

Para problemas o mejoras, revisa el código en `app.py`
