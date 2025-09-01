import streamlit as st
import pandas as pd
import altair as alt
import os
import hashlib

# Archivos y carpetas
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "registros.csv")
VARIEDADES_FILE = os.path.join(DATA_FOLDER, "variedades.csv")
MODULOS_FILE = os.path.join(DATA_FOLDER, "modulos.csv")
RESPONSABLES_FILE = os.path.join(DATA_FOLDER, "responsables.csv")
ELIMINADOS_FILE = os.path.join(DATA_FOLDER, "eliminados.csv")

# === FUNCIONES DE AUTENTICACIÓN ===
def verificar_credenciales(usuario, contraseña):
    """Verificar si las credenciales son válidas"""
    if os.path.exists(RESPONSABLES_FILE):
        df = pd.read_csv(RESPONSABLES_FILE)
        # Buscar el usuario
        user_row = df[df['Usuario'] == usuario]
        if not user_row.empty:
            # Verificar contraseña (convertir a string para evitar problemas de tipo)
            stored_password = str(user_row.iloc[0]['Contraseña']).strip()
            input_password = str(contraseña).strip()
            if stored_password == input_password:
                return {
                    'nombre': user_row.iloc[0]['Responsable'],
                    'usuario': user_row.iloc[0]['Usuario'],
                    'rol': user_row.iloc[0]['Rol']
                }
    return None

def mostrar_login():
    """Mostrar la pantalla de login"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🌸 SISTEMA DE COSECHA</h1>
        <h3>Ingreso de Trabajadores</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### 🔐 Iniciar Sesión")
        usuario = st.text_input("👤 Usuario")
        contraseña = st.text_input("🔑 Contraseña", type="password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button("Ingresar", use_container_width=True)
        
        if login_button:
            if usuario and contraseña:
                user_info = verificar_credenciales(usuario, contraseña)
                if user_info:
                    st.session_state.logged_in = True
                    st.session_state.user_info = user_info
                    st.success(f"¡Bienvenido/a, {user_info['nombre']}!")
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
            else:
                st.warning("⚠️ Por favor, complete todos los campos")
    
    # Información de acceso
    with st.expander("ℹ️ Información de acceso"):
        st.markdown("""
        **Usuarios de ejemplo:**
        - **Administrador:** usuario: `rene`, contraseña: `1234`
        - **Trabajador:** usuario: `marcia`, contraseña: `123456`
        - **Trabajador:** usuario: `kevin`, contraseña: `123456`
        
        **Permisos:**
        - **Admin:** Puede registrar, ver, eliminar registros
        - **Trabajador:** Puede registrar y ver registros
        """)

def logout():
    """Cerrar sesión"""
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.rerun()

def mostrar_info_usuario():
    """Mostrar información del usuario logueado"""
    if 'user_info' in st.session_state:
        user = st.session_state.user_info
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"👤 **{user['nombre']}** ({user['rol']})")
        
        with col2:
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                logout()

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

# Cargar responsables
def load_responsables():
    if os.path.exists(RESPONSABLES_FILE):
        df = pd.read_csv(RESPONSABLES_FILE)
        return df["Responsable"].dropna().unique().tolist()
    else:
        return []

# Cargar datos existentes
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Fecha", "Hora", "Fecha_Formato", "Numero_Viaje", "Responsable", "Variedad", "Mallas", "Número de tallos", "Total cosecha", "Modulo"])

# Guardar nuevo registro
def save_data(new_record):
    existing_data = load_data()
    existing_data = pd.concat([existing_data, pd.DataFrame([new_record])], ignore_index=True)
    existing_data.to_csv(DATA_FILE, index=False)

# Guardar registro eliminado
def save_deleted_record(deleted_record):
    from datetime import datetime
    
    # Agregar información de eliminación
    deleted_record_with_info = deleted_record.copy()
    deleted_record_with_info['Fecha_Eliminacion'] = datetime.now().strftime("%Y-%m-%d")
    deleted_record_with_info['Hora_Eliminacion'] = datetime.now().strftime("%H:%M:%S")
    deleted_record_with_info['Motivo'] = "Eliminado manualmente"
    
    # Cargar datos eliminados existentes o crear estructura
    if os.path.exists(ELIMINADOS_FILE):
        deleted_data = pd.read_csv(ELIMINADOS_FILE)
    else:
        # Crear DataFrame con las columnas originales más las nuevas
        columns = ["Fecha", "Hora", "Fecha_Formato", "Numero_Viaje", "Responsable", "Variedad", 
                  "Mallas", "Número de tallos", "Total cosecha", "Modulo", 
                  "Fecha_Eliminacion", "Hora_Eliminacion", "Motivo"]
        deleted_data = pd.DataFrame(columns=columns)
    
    # Agregar el nuevo registro eliminado
    deleted_data = pd.concat([deleted_data, pd.DataFrame([deleted_record_with_info])], ignore_index=True)
    deleted_data.to_csv(ELIMINADOS_FILE, index=False)

# Crear carpeta si no existe
os.makedirs(DATA_FOLDER, exist_ok=True)

# Configuración de página para móviles
st.set_page_config(
    page_title="Registro de Cosecha",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === CONTROL DE ACCESO ===
# Inicializar estado de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Si no está logueado, mostrar pantalla de login
if not st.session_state.logged_in:
    mostrar_login()
    st.stop()

# Si está logueado, mostrar la aplicación principal
mostrar_info_usuario()

# Información del sistema
st.sidebar.markdown("### Sistema de Cosecha")
st.sidebar.markdown("**Versión:** 1.0")
st.sidebar.markdown("**Optimizado para móviles**")
if 'user_info' in st.session_state:
    st.sidebar.markdown(f"**Usuario:** {st.session_state.user_info['nombre']}")
    st.sidebar.markdown(f"**Rol:** {st.session_state.user_info['rol']}")

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
    # Primera fila - Fecha y Hora
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha de cosecha")
    with col2:
        hora = st.time_input("Hora de cosecha")

    # Campo automático de semana en formato AA-SS (no editable)
    fecha_formato_auto = fecha.strftime("%y%U")  # Año de 2 dígitos + semana del año
    st.text_input("Semana", value=fecha_formato_auto, disabled=True, 
                  help="Formato automático: Año (2 dígitos) + Semana del año")

    # Segunda fila - Número de viaje
    numero_viaje = st.number_input("Número de viaje", min_value=1, step=1, value=1)

    # Tercera fila - Responsable y Módulo
    col3, col4 = st.columns(2)
    with col3:
        responsables = load_responsables()
        if responsables:
            responsable = st.selectbox("Responsable", ["Seleccione responsable..."] + responsables, index=0)
            if responsable == "Seleccione responsable...":
                responsable = ""
        else:
            st.warning("No hay responsables disponibles en data/responsables.csv")
            responsable = ""
    with col4:
        # Módulo
        modulos = load_modulos()
        if modulos:
            modulo = st.selectbox("Módulo", ["Seleccione módulo..."] + modulos, index=0)
            if modulo == "Seleccione módulo...":
                modulo = ""
        else:
            st.warning("No hay módulos disponibles en data/modulos.csv")
            modulo = ""

    # Variedad (ancho completo para mejor legibilidad en móvil)
    variedades = load_variedades()
    if variedades:
        variedad = st.selectbox("Variedad", ["Seleccione variedad..."] + variedades, index=0)
        if variedad == "Seleccione variedad...":
            variedad = ""
    else:
        st.warning("No hay variedades disponibles en data/variedades.csv")
        variedad = ""

    # Cuarta fila - Mallas y tallos por malla
    col5, col6 = st.columns(2)
    with col5:
        mallas = st.number_input("Número de mallas", min_value=1, step=1)
    with col6:
        num_tallos = st.selectbox("Tallos por malla", [10, 15, 20, 25, 30])
    
    # Cálculo automático
    total_cosecha = mallas * num_tallos
    st.info(f"**Total cosecha calculada: {total_cosecha:,} tallos**")

    enviado = st.form_submit_button("Registrar Cosecha", use_container_width=True)

    if enviado:
        if not variedad or not modulo or not responsable:
            st.error("Debe completar todos los campos obligatorios.")
        else:            
            registro = {
                "Fecha": fecha.strftime("%Y-%m-%d"),
                "Hora": hora.strftime("%H:%M"),
                "Fecha_Formato": fecha_formato_auto,
                "Numero_Viaje": numero_viaje,
                "Responsable": responsable,
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
    # Reordenar columnas para mejor visualización
    cols = data.columns.tolist()
    orden_preferido = ["Fecha_Formato", "Fecha", "Hora", "Numero_Viaje", "Responsable", "Modulo", "Variedad", "Mallas", "Número de tallos", "Total cosecha"]
    cols_ordenadas = [col for col in orden_preferido if col in cols] + [col for col in cols if col not in orden_preferido]
    data = data[cols_ordenadas]
    
    # Columnas a ocultar en la visualización
    columnas_ocultar = ["Número de mallas", "Tallos por malla"]

    # Filtros
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        modulos_unicos = data["Modulo"].dropna().unique().tolist()
        modulo_filtro = st.selectbox("Filtrar por módulo", ["Todos"] + modulos_unicos)
    with col_filtro2:
        if "Responsable" in data.columns:
            responsables_unicos = data["Responsable"].dropna().unique().tolist()
            responsable_filtro = st.selectbox("Filtrar por responsable", ["Todos"] + responsables_unicos)
        else:
            responsable_filtro = "Todos"
    
    # Aplicar filtros
    data_filtrada = data.copy()
    if modulo_filtro != "Todos":
        data_filtrada = data_filtrada[data_filtrada["Modulo"] == modulo_filtro]
    if responsable_filtro != "Todos" and "Responsable" in data.columns:
        data_filtrada = data_filtrada[data_filtrada["Responsable"] == responsable_filtro]
    
    data_filtrada = data_filtrada.reset_index(drop=True)

    # Mostrar resumen para móviles
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Registros", len(data_filtrada))
    with col2:
        if "Total cosecha" in data_filtrada.columns:
            st.metric("Total Tallos", f"{data_filtrada['Total cosecha'].sum():,.0f}")
    with col3:
        if "Variedad" in data_filtrada.columns:
            st.metric("Variedades", data_filtrada['Variedad'].nunique())
    with col4:
        if "Numero_Viaje" in data_filtrada.columns:
            st.metric("Viajes", data_filtrada['Numero_Viaje'].nunique())

    # --- MOSTRAR GRÁFICO DE TALLOS POR VARIEDAD ---
    st.subheader("Registros guardados - Total de tallos")
    if not data_filtrada.empty and "Variedad" in data_filtrada.columns and "Total cosecha" in data_filtrada.columns:
        # Preparar datos para el gráfico
        tallos_por_variedad_grafico = data_filtrada.groupby("Variedad")["Total cosecha"].sum().reset_index()
        tallos_por_variedad_grafico = tallos_por_variedad_grafico.sort_values("Total cosecha", ascending=False)
        
        # Crear gráfico de barras
        chart = alt.Chart(tallos_por_variedad_grafico).mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3,
            color='#1f77b4'
        ).encode(
            x=alt.X("Variedad:N", 
                   sort="-y",
                   axis=alt.Axis(labelAngle=-45, labelFontSize=12, title="Variedad")),
            y=alt.Y("Total cosecha:Q",
                   axis=alt.Axis(labelFontSize=12, title="Total de tallos")),
            tooltip=["Variedad:N", alt.Tooltip("Total cosecha:Q", format=".0f", title="Total tallos")]
        ).properties(
            width="container",
            height=400,
            title=alt.TitleParams(
                text="Total de tallos por variedad",
                fontSize=16,
                fontWeight="bold"
            )
        )

        # Agregar etiquetas en las barras
        etiquetas = alt.Chart(tallos_por_variedad_grafico).mark_text(
            align='center', 
            dy=-10, 
            color='black',
            fontSize=12,
            fontWeight='bold'
        ).encode(
            x=alt.X("Variedad:N", sort="-y"),
            y="Total cosecha:Q",
            text=alt.Text("Total cosecha:Q", format=".0f")
        )

        # Combinar gráfico y etiquetas
        final_chart = (chart + etiquetas).resolve_scale(
            color='independent'
        )
        
        # Mostrar el gráfico
        st.altair_chart(final_chart, use_container_width=True)
        
        # Mostrar también tabla resumen debajo del gráfico
        st.markdown("##### Resumen numérico:")
        col_tabla1, col_tabla2 = st.columns(2)
        for i, (_, row) in enumerate(tallos_por_variedad_grafico.iterrows()):
            if i % 2 == 0:
                with col_tabla1:
                    st.metric(row['Variedad'], f"{row['Total cosecha']:,} tallos")
            else:
                with col_tabla2:
                    st.metric(row['Variedad'], f"{row['Total cosecha']:,} tallos")
    else:
        st.info("No hay registros para mostrar el gráfico.")

    # --- TABLA DE REGISTROS CON OPCIÓN DE ELIMINAR ---
    st.subheader("Tabla de registros")
    st.markdown("##### Todos los registros guardados:")
    
    if not data_filtrada.empty:
        # Mostrar tabla completa
        st.dataframe(data_filtrada, use_container_width=True, height=400)
        
        # Sección para eliminar registros - SOLO PARA ADMINISTRADORES
        if st.session_state.user_info['rol'] == 'admin':
            st.markdown("---")
            st.markdown("##### 🗑️ Eliminar registro")
            st.markdown("**Seleccione el registro que desea eliminar:**")
        
        # Crear opciones para el selectbox con información detallada
        opciones_eliminar = []
        for idx in range(len(data_filtrada)):
            row = data_filtrada.iloc[idx]
            semana = row.get('Fecha_Formato', 'N/A')
            fecha = row.get('Fecha', 'N/A')
            hora = row.get('Hora', 'N/A')
            responsable = row.get('Responsable', 'N/A')
            variedad = row.get('Variedad', 'N/A')
            modulo = row.get('Modulo', 'N/A')
            total = row.get('Total cosecha', 'N/A')
            viaje = row.get('Numero_Viaje', 'N/A')
            
            opcion = f"Registro {idx + 1}: Sem.{semana} | {fecha} {hora} | Viaje:{viaje} | {responsable} | {variedad} | {modulo} | {total} tallos"
            opciones_eliminar.append(opcion)
        
        # Selectbox para elegir qué registro eliminar
        col_select, col_button = st.columns([3, 1])
        
        with col_select:
            if opciones_eliminar:
                registro_a_eliminar = st.selectbox(
                    "Registro a eliminar:",
                    options=[None] + list(range(len(opciones_eliminar))),
                    format_func=lambda x: "Seleccione un registro..." if x is None else opciones_eliminar[x],
                    help="Seleccione el registro que desea eliminar de la lista",
                    index=0  # Inicia en None (vacío)
                )
        
        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)  # Espacio para alinear
            if st.button("🗑️ Eliminar", type="primary", use_container_width=True):
                if registro_a_eliminar is not None:
                    # Obtener el registro seleccionado de la data filtrada
                    row_a_eliminar = data_filtrada.iloc[registro_a_eliminar]
                    
                    # Cargar todos los datos (sin filtros) para encontrar el registro exacto
                    data_completa = load_data()
                    
                    # Buscar el registro en la data completa usando múltiples criterios
                    condicion = (
                        (data_completa['Fecha'] == row_a_eliminar['Fecha']) &
                        (data_completa['Hora'] == row_a_eliminar['Hora']) &
                        (data_completa['Variedad'] == row_a_eliminar['Variedad']) &
                        (data_completa['Modulo'] == row_a_eliminar['Modulo']) &
                        (data_completa['Total cosecha'] == row_a_eliminar['Total cosecha']) &
                        (data_completa['Numero_Viaje'] == row_a_eliminar['Numero_Viaje'])
                    )
                    
                    # Encontrar índices que coinciden
                    indices_coincidentes = data_completa[condicion].index
                    
                    if len(indices_coincidentes) > 0:
                        # Obtener el registro completo que se va a eliminar
                        indice_a_eliminar = indices_coincidentes[0]
                        registro_a_guardar = data_completa.iloc[indice_a_eliminar]
                        
                        # Guardar el registro en eliminados.csv ANTES de eliminarlo
                        save_deleted_record(registro_a_guardar)
                        
                        # Eliminar el registro del archivo principal
                        data_actualizada = data_completa.drop(indice_a_eliminar).reset_index(drop=True)
                        
                        # Guardar los datos actualizados
                        data_actualizada.to_csv(DATA_FILE, index=False)
                        
                        st.success(f"✅ Registro eliminado exitosamente: {row_a_eliminar['Variedad']} - {row_a_eliminar['Fecha']} {row_a_eliminar['Hora']}")
                        st.info(f"📁 El registro ha sido guardado en eliminados.csv como respaldo")
                        st.rerun()
                    else:
                        st.error("❌ No se pudo encontrar el registro para eliminar")
        
        # Mostrar detalles del registro seleccionado
        if registro_a_eliminar is not None and len(data_filtrada) > 0:
            st.markdown("---")
            st.markdown("##### 📋 Detalles del registro seleccionado:")
            row_seleccionada = data_filtrada.iloc[registro_a_eliminar]
            
            col_det1, col_det2, col_det3 = st.columns(3)
            with col_det1:
                st.info(f"**📅 Fecha:** {row_seleccionada.get('Fecha', 'N/A')}")
                st.info(f"**🕐 Hora:** {row_seleccionada.get('Hora', 'N/A')}")
                st.info(f"**📊 Semana:** {row_seleccionada.get('Fecha_Formato', 'N/A')}")
            
            with col_det2:
                st.info(f"**🚛 Viaje:** {row_seleccionada.get('Numero_Viaje', 'N/A')}")
                st.info(f"**👤 Responsable:** {row_seleccionada.get('Responsable', 'N/A')}")
                st.info(f"**🏠 Módulo:** {row_seleccionada.get('Modulo', 'N/A')}")
            
            with col_det3:
                st.info(f"**🌸 Variedad:** {row_seleccionada.get('Variedad', 'N/A')}")
                st.info(f"**📦 Mallas:** {row_seleccionada.get('Mallas', 'N/A')}")
                st.info(f"**🎯 Total:** {row_seleccionada.get('Total cosecha', 'N/A')} tallos")
        else:
            st.markdown("---")
            st.info("🔒 Solo los administradores pueden eliminar registros.")
    
    else:
        st.info("No hay registros disponibles para mostrar.")

# --- INFORMACIÓN DE REGISTROS ELIMINADOS (SOLO ADMIN) ---
if st.session_state.user_info['rol'] == 'admin':
    st.markdown("---")
    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("##### 📊 Estadísticas de eliminación")
        if os.path.exists(ELIMINADOS_FILE):
            deleted_data = pd.read_csv(ELIMINADOS_FILE)
            if not deleted_data.empty:
                st.metric("Total eliminados", len(deleted_data))
                if 'Fecha_Eliminacion' in deleted_data.columns:
                    last_deletion = deleted_data['Fecha_Eliminacion'].iloc[-1]
                    st.metric("Última eliminación", last_deletion)
            else:
                st.metric("Total eliminados", 0)
        else:
            st.metric("Total eliminados", 0)

    with col_info2:
        st.markdown("##### 📁 Archivo de respaldo")
        st.info("Los registros eliminados se guardan automáticamente en:")
        st.code("data/eliminados.csv")
        st.markdown("Este archivo contiene:")
        st.markdown("• Todos los datos originales")
        st.markdown("• Fecha y hora de eliminación") 
        st.markdown("• Motivo de la eliminación")
else:
    st.markdown("---")
    st.info("🔒 Las estadísticas de eliminación solo están disponibles para administradores.")
