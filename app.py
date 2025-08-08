import streamlit as st
import pandas as pd
import altair as alt
import os

# Archivos y carpetas
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "registros.csv")
VARIEDADES_FILE = os.path.join(DATA_FOLDER, "variedades.csv")
MODULOS_FILE = os.path.join(DATA_FOLDER, "modulos.csv")

# Cargar variedades
def load_variedades():
    if os.path.exists(VARIEDADES_FILE):
        df = pd.read_csv(VARIEDADES_FILE)
        return df["Variedad"].dropna().unique().tolist()
    else:
        return []

# Cargar módulos
def load_modulos():
    if os.path.exists(MODULOS_FILE):
        df = pd.read_csv(MODULOS_FILE)
        return df["Modulo"].dropna().unique().tolist()
    else:
        return []

# Cargar datos existentes
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Fecha", "Variedad", "Mallas", "Número de tallos", "Total cosecha", "Modulo"])

# Guardar nuevo registro
def save_data(new_record):
    existing_data = load_data()
    existing_data = pd.concat([existing_data, pd.DataFrame([new_record])], ignore_index=True)
    existing_data.to_csv(DATA_FILE, index=False)

# Crear carpeta si no existe
os.makedirs(DATA_FOLDER, exist_ok=True)

# Configuración de página para móviles
st.set_page_config(
    page_title="Registro de Cosecha",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Información del sistema
st.sidebar.markdown("### Sistema de Cosecha")
st.sidebar.markdown("**Versión:** 1.0")
st.sidebar.markdown("**Optimizado para móviles**")

# CSS personalizado para móviles
st.markdown("""
<style>
    .main > div {
        padding: 1rem;
    }
    
    .stSelectbox > div > div {
        font-size: 16px;
    }
    
    .stNumberInput > div > div > input {
        font-size: 16px;
    }
    
    .stDateInput > div > div > input {
        font-size: 16px;
    }
    
    @media (max-width: 768px) {
        .stForm {
            padding: 0.5rem;
        }
        
        .stDataFrame {
            font-size: 12px;
        }
        
        .stSelectbox > div > div {
            font-size: 14px;
        }
        
        .stNumberInput > div > div > input {
            font-size: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Título de la app
st.title("REGISTRO DE COSECHA")

# --- FORMULARIO ---
st.subheader("Nuevo Registro")
with st.form("formulario_cosecha"):
    # Primera fila
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha de cosecha")
    with col2:
        # Módulo
        modulos = load_modulos()
        if modulos:
            modulo = st.selectbox("Módulo", modulos)
        else:
            st.warning("No hay módulos disponibles en data/modulos.csv")
            modulo = ""

    # Variedad (ancho completo para mejor legibilidad en móvil)
    variedades = load_variedades()
    if variedades:
        variedad = st.selectbox("Variedad", variedades)
    else:
        st.warning("No hay variedades disponibles en data/variedades.csv")
        variedad = ""

    # Tercera fila
    col3, col4 = st.columns(2)
    with col3:
        mallas = st.number_input("Número de mallas", min_value=1, step=1)
    with col4:
        num_tallos = st.selectbox("Tallos por malla", [10, 15, 20, 25, 30])
    
    # Cálculo automático
    total_cosecha = mallas * num_tallos
    st.info(f"**Total cosecha calculada: {total_cosecha:,} tallos**")

    enviado = st.form_submit_button("Registrar Cosecha", use_container_width=True)

    if enviado:
        if not variedad or not modulo:
            st.error("Debe seleccionar una variedad y un módulo.")
        else:
            registro = {
                "Fecha": fecha.strftime("%Y-%m-%d"),
                "Variedad": variedad,
                "Mallas": mallas,
                "Número de tallos": num_tallos,
                "Total cosecha": total_cosecha,
                "Modulo": modulo
            }
            save_data(registro)
            st.success("Registro guardado exitosamente.")


# --- MOSTRAR DATOS Y GESTIÓN DE REGISTROS ---
st.subheader("Registros guardados")
data = load_data()

if data.empty:
    st.info("No hay registros aún.")
else:
    # Reordenar columnas: Modulo primero
    cols = data.columns.tolist()
    if "Modulo" in cols:
        cols.remove("Modulo")
        cols.insert(0, "Modulo")
        data = data[cols]

    # Filtro por módulo
    modulos_unicos = data["Modulo"].dropna().unique().tolist()
    modulo_filtro = st.selectbox("Filtrar por módulo", ["Todos"] + modulos_unicos)
    if modulo_filtro != "Todos":
        data_filtrada = data[data["Modulo"] == modulo_filtro].reset_index(drop=True)
    else:
        data_filtrada = data.reset_index(drop=True)

    # Mostrar resumen para móviles
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(data_filtrada))
    with col2:
        if "Total cosecha" in data_filtrada.columns:
            st.metric("Total Tallos", f"{data_filtrada['Total cosecha'].sum():,.0f}")
    with col3:
        if "Variedad" in data_filtrada.columns:
            st.metric("Variedades", data_filtrada['Variedad'].nunique())

    # Tabla de registros y eliminación
    st.markdown("#### Eliminar registro")
    if not data_filtrada.empty:
        
        # Mostrar tabla de solo lectura
        st.dataframe(data_filtrada, use_container_width=True, height=300)
        
        # Barra de búsqueda para seleccionar registro a eliminar
        st.markdown("##### Buscar y eliminar registro:")
        
        # Crear opciones de búsqueda con información detallada
        opciones_busqueda = []
        for idx, row in data_filtrada.iterrows():
            opcion = f"Fila {idx}: {row['Fecha']} | {row['Variedad']} | {row['Modulo']} | {row['Total cosecha']} tallos"
            opciones_busqueda.append(opcion)
        
        # Selectbox con búsqueda
        registro_seleccionado = st.selectbox(
            "Busque el registro que desea eliminar:",
            options=range(len(data_filtrada)),
            format_func=lambda x: opciones_busqueda[x],
            help="Use este campo para buscar y seleccionar el registro a eliminar"
        )
        
        # Mostrar detalles del registro seleccionado
        if registro_seleccionado is not None:
            row_seleccionada = data_filtrada.iloc[registro_seleccionado]
            st.info(f"**Registro seleccionado:**\n"
                   f"📅 Fecha: {row_seleccionada['Fecha']}\n"
                   f"🌸 Variedad: {row_seleccionada['Variedad']}\n"
                   f"🏠 Módulo: {row_seleccionada['Modulo']}\n"
                   f"📦 Mallas: {row_seleccionada['Mallas']}\n"
                   f"🌾 Tallos por malla: {row_seleccionada['Número de tallos']}\n"
                   f"🎯 Total cosecha: {row_seleccionada['Total cosecha']} tallos")
        
        # Botón de eliminación
        if st.button("🗑️ Eliminar registro seleccionado", use_container_width=True, type="primary"):
            data_actualizada = data.copy()
            
            if modulo_filtro != "Todos":
                # Obtener índice real en el dataframe original
                idx_original = data[data["Modulo"] == modulo_filtro].index[registro_seleccionado]
            else:
                idx_original = registro_seleccionado
            
            # Eliminar registro
            data_actualizada = data_actualizada.drop(idx_original).reset_index(drop=True)
            data_actualizada.to_csv(DATA_FILE, index=False)
            
            st.success("✅ Registro eliminado correctamente")
            st.rerun()
    else:
        st.info("No hay registros para este módulo.")

# --- GRÁFICO TOTAL TALLOS POR VARIEDAD CON ETIQUETAS ---
st.subheader("Total de tallos por variedad")

if not data.empty:
    tallos_por_variedad = data.groupby("Variedad")["Total cosecha"].sum().reset_index()

    # Configuración responsiva del gráfico
    base_width = 400
    base_height = 300
    
    chart = alt.Chart(tallos_por_variedad).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x=alt.X("Variedad", 
               sort="-y",
               axis=alt.Axis(labelAngle=-45, labelFontSize=10)),
        y=alt.Y("Total cosecha",
               axis=alt.Axis(labelFontSize=10)),
        color=alt.Color("Variedad", legend=None),
        tooltip=["Variedad", "Total cosecha"]
    ).properties(
        width=base_width,
        height=base_height
    )

    etiquetas = alt.Chart(tallos_por_variedad).mark_text(
        align='center', 
        dy=-10, 
        color='black',
        fontSize=10
    ).encode(
        x="Variedad",
        y="Total cosecha",
        text=alt.Text("Total cosecha:Q", format=".0f")
    )

    final_chart = (chart + etiquetas).resolve_scale(
        color='independent'
    )
    
    st.altair_chart(final_chart, use_container_width=True)
else:
    st.info("No hay datos para graficar.")
