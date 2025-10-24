import streamlit as st
from app.Inscripcion import inscribirse_a_actividad
from app.DB import crear_tablas, inicializar_actividades, obtener_actividades,rollback, start_transaction, commit

# Configuración de la página
st.set_page_config(page_title="Inscripción a Actividades", page_icon="🎯")
st.title("🎯 Sistema de Inscripción a Actividades")

# Inicializar estado de la sesión
if "inscripcion_exitosa" not in st.session_state:
    st.session_state.inscripcion_exitosa = False

if st.session_state.inscripcion_exitosa:
    st.success("🎉 ¡Inscripción exitosa!")
    st.write("Ya se ha realizado una inscripción exitosa en esta sesión, presione volver a inscribir para realizar una nueva inscripción.")
    if st.button("Volver a inscribir", key="btn_volver_inscribir"):
        st.session_state.inscripcion_exitosa = False
        # Refrescar actividades desde la base
        actividades = obtener_actividades()
        # Resetear campos
        cantidad = 1
        nombre = None
        dni = None
        edad = None
        terminos_aceptados = False
        st.rerun()
    st.stop()

def init_db():
    # Crear tablas si no existen
    crear_tablas()
    # Inicializar actividades si no existen
    inicializar_actividades()

# Inicializar la base
init_db()
start_transaction()

# Obtener actividades del back (base de datos)
actividades = obtener_actividades()

# --- Sección de selección de actividad ---
st.header("🏃 Selección de Actividad")
actividades_disponibles = list(actividades.keys())
nombre_actividad = st.selectbox(
    "Seleccione una actividad *",
    options=actividades_disponibles,
    help="Elija la actividad en la que desea inscribirse"
)

# Mostrar información de la actividad seleccionada
actividad_info = actividades.get(nombre_actividad)
indice_horario = 0
cupo_disponible = 0
if actividad_info:
    # Construir lista de horarios para el selectbox y cupos
    horarios_disponibles = [h["hora"] for h in actividad_info["horarios"]]
    cupos = [h["cupo"] for h in actividad_info["horarios"]]
    st.info(f"🕐 Horarios: {', '.join(horarios_disponibles)}")

# Selección de horario
horario = st.selectbox(
    "Seleccione un horario *",
    options=horarios_disponibles if actividad_info else [],
    help="Elija el horario que mejor le convenga"
)

# Determinar índice del horario seleccionado y cupo disponible
if actividad_info and horario in horarios_disponibles:
    indice_horario = horarios_disponibles.index(horario)
    cupo_disponible = cupos[indice_horario]
    st.info(f"📊 Cupos disponibles: {cupo_disponible}")

# Cantidad de participantes
cantidad = st.number_input(
    "Cantidad de participantes *",
    min_value=1,
    step=1
)

# Sección de datos de los participantes
st.header("📋 Datos de los Participantes")
participantes = []
for i in range(cantidad):
    st.subheader(f"👤 Participante {i+1}")
    nombre = st.text_input(f"Nombre completo (Participante {i+1}) *")
    dni = st.text_input(f"DNI (Participante {i+1}) *")
    edad = st.number_input(f"Edad (Participante {i+1}) *", step=1)
    talle = None
    if actividad_info and actividad_info.get("requiere_talle", False):
        talle = st.selectbox(f"Talle (Participante {i+1}) *", options=["XS", "S", "M", "L", "XL", "XXL"])
    participantes.append({"nombre": nombre, "dni": dni, "edad": edad, "talle": talle})

# Términos y condiciones
st.header("📜 Términos y Condiciones")
terminos_aceptados = st.checkbox(f"Acepto los términos y condiciones de {nombre_actividad} *")

with st.expander("Ver términos y condiciones"):
    if actividad_info:
        st.markdown(actividad_info["terminos"])

# Botón de inscripción
st.divider()
if st.button("✅ Inscribirse", type="primary", use_container_width=True, key="btn_inscribirse"):
    if st.session_state.inscripcion_exitosa:
        st.stop()
    else:
        try:
            for participante in participantes:
                resultado = inscribirse_a_actividad(
                    actividades=actividades,
                    nombre_actividad=nombre_actividad,
                    visitante=participante,
                    terminos_aceptados=terminos_aceptados,
                    horario=horario,
                    cantidad=1,
                )

            #commit
            commit()
            
            st.session_state.inscripcion_exitosa = True
            st.success("🎉 ¡Inscripción exitosa!")
            st.balloons()
            st.subheader("📄 Resumen de Inscripción")
            st.write(f"**Actividad:** {nombre_actividad}")
            st.write(f"**Horario:** {horario}")
            for idx, p in enumerate(participantes):
                st.write(f"**Participante {idx+1}:** {p['nombre']}, DNI: {p['dni']}, Edad: {p['edad']}, Talle: {p.get('talle', 'N/A')}")
            st.info(f"Cupos restantes: {actividad_info['horarios'][indice_horario]['cupo']}")

        except Exception as e:
            st.error(f"❌ Error en la inscripción: {str(e)}")
            #rollback
            rollback()
            actividades = obtener_actividades()

# Footer
st.divider()
st.caption("Sistema de Inscripción a Actividades v1.0")