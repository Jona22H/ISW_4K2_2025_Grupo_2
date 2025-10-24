# app/inscripcion.py
from app import DB as db
from app.Validaciones import validar_cupos, validar_edad, validar_nombre, validar_dni, validar_talle, validar_horarios_disponibles, validar_horario_elegido, validar_terminos_y_condiciones, validar_seleccion_de_actividad, validar_que_actividad_exista

def inscribirse_a_actividad(actividades, nombre_actividad, visitante, terminos_aceptados, horario, cantidad):
    """
    Permite a un visitante inscribirse en una actividad si hay cupos y acepta los términos.
    Valida talle si la actividad lo requiere, verifica campos obligatorios y el horario seleccionado.
    """
    db.start_transaction()

    # --- Validaciones iniciales ---

    validar_terminos_y_condiciones(terminos_aceptados)
    validar_seleccion_de_actividad(nombre_actividad)
    validar_que_actividad_exista(actividades, nombre_actividad)

    actividad = actividades[nombre_actividad]

    # --- Validar horarios ---
    validar_horarios_disponibles(actividad.get("horarios", []))

    # Buscar el horario elegido dentro de la lista
    horario_encontrado = validar_horario_elegido(horario, actividad.get("horarios"))


    # --- Validar cupos ---
    validar_cupos(horario_encontrado["cupo"], cantidad)

    # --- Validar visitante ---

    validar_nombre(visitante.get("nombre"))
    validar_edad(visitante.get("edad"))
    validar_dni(visitante.get("dni"))

    # --- Validar talle (si aplica) ---
    if actividad.get("requiere_talle", False):
        validar_talle(visitante)

    # --- Registrar participantes en BD ---
    for _ in range(cantidad):
        db.guardar_participante(visitante, nombre_actividad, horario)

    # --- Actualizar cupo del horario ---
    horario_encontrado["cupo"] -= cantidad
    db.actualizar_cupo_por_horario(nombre_actividad, horario, horario_encontrado["cupo"])

    # --- Confirmar transacción ---
    db.commit()

    # --- Retornar resultado ---
    return {
        "actividad": nombre_actividad,
        "visitante": visitante,
        "horario": horario,
        "cantidad": cantidad
    }
