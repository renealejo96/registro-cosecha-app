import streamlit as st

st.set_page_config(
    page_title="🌸 Registro de Cosecha",
    page_icon="🌸",
    layout="wide"
)

st.markdown("""
# 🌸 Sistema de Registro de Cosecha

## 📱 Instrucciones de Uso

1. **Fecha**: Selecciona la fecha de cosecha
2. **Variedad**: Elige la variedad de flor
3. **Módulo**: Selecciona el módulo de producción
4. **Mallas**: Ingresa el número de mallas cosechadas
5. **Tallos por malla**: Selecciona la cantidad de tallos por malla

### 📊 Funcionalidades:
- ✅ Registro automático de datos
- 📈 Gráficos de producción por variedad
- 📋 Historial de registros
- 📱 Optimizado para móviles

---
**Para comenzar, usa el menú lateral o navega a la página principal.**
""")

# Botón para ir a la aplicación principal
if st.button("🚀 Ir a la Aplicación Principal", use_container_width=True):
    st.switch_page("app.py")
