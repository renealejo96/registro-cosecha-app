# 🌸 Aplicación de Registro de Cosecha

Una aplicación web desarrollada con Streamlit para registrar y visualizar datos de cosecha de flores.

## 🚀 Características

- ✅ Registro de cosecha por fecha, variedad y módulo
- 📊 Visualización gráfica de datos
- 📱 Interfaz optimizada para dispositivos móviles
- 📋 Tabla de registros guardados
- 🔢 Métricas de resumen

## 📦 Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Ejecución

### Opción 1: Script automático (Windows)
```bash
run_app.bat
```

### Opción 2: Comando manual
```bash
streamlit run app.py
```

### Opción 3: Para acceso desde móviles en la red local
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 📱 Acceso desde Móvil

1. Ejecuta la aplicación con la opción 3
2. Encuentra la IP de tu computadora:
   - Windows: `ipconfig`
   - En la red Wi-Fi busca "IPv4 Address"
3. En tu móvil, abre el navegador y ve a: `http://[IP_DE_TU_PC]:8501`
   - Ejemplo: `http://192.168.1.100:8501`

## 📁 Estructura de Archivos

```
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── run_app.bat           # Script de inicio (Windows)
├── .streamlit/
│   └── config.toml       # Configuración de Streamlit
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
