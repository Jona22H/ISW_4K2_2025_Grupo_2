# app/inscripcion.py
from app import db

def inscribirse_a_actividad(actividades, nombre_actividad, visitante, terminos_aceptados, horario, cantidad):
    """
    Permite a un visitante inscribirse en una actividad si hay cupos y acepta los términos.
    Valida talle si la actividad lo requiere, verifica campos obligatorios y el horario seleccionado.
    """

    # --- Validaciones iniciales ---
    if not terminos_aceptados:
        raise Exception("Debe aceptar los términos y condiciones")

    if not nombre_actividad:
        raise Exception("Debe seleccionar una actividad")

    if nombre_actividad not in actividades:
        raise Exception("La actividad seleccionada no existe")

    actividad = actividades[nombre_actividad]

    # --- Validar horarios ---
    horarios_disponibles = actividad.get("horarios")
    if not horarios_disponibles:
        raise Exception("No hay horarios disponibles para la actividad seleccionada")

    # Buscar el horario elegido dentro de la lista
    horario_encontrado = None
    for h in horarios_disponibles:
        if h["hora"] == horario:
            horario_encontrado = h
            break

    if not horario_encontrado:
        raise Exception("Horario no disponible")

    # --- Validar cupos ---
    cupo_disponible = horario_encontrado["cupo"]

    if not isinstance(cantidad, int) or cantidad <= 0:
        raise Exception("Debe indicar una cantidad válida de participantes")

    if cupo_disponible < cantidad:
        raise Exception("No hay suficientes cupos disponibles para la cantidad de participantes solicitada")

    # --- Validar visitante ---
    campos_obligatorios = ["nombre", "dni", "edad"]
    for campo in campos_obligatorios:
        if campo not in visitante or visitante[campo] in [None, "", 0]:
            raise Exception(f"El campo '{campo}' es obligatorio")

    edad = visitante.get("edad")
    if not (1 <= edad <= 99):
        raise Exception("La edad debe estar entre 1 y 99 años")

    dni = visitante.get("dni")
    if not dni or not dni.isdigit() or int(dni) <= 0:
        raise Exception("El DNI debe ser un número positivo")

    # --- Validar talle (si aplica) ---
    if actividad.get("requiere_talle", False):
        if "talle" not in visitante or not visitante["talle"]:
            raise Exception("Debe ingresar el talle de vestimenta requerido por la actividad")

        talles_permitidos = ["XS", "S", "M", "L", "XL", "XXL"]
        if visitante["talle"] not in talles_permitidos:
            raise Exception("El talle ingresado no es válido")

    # --- Registrar participantes en BD ---
    for _ in range(cantidad):
        db.guardar_participante(visitante, nombre_actividad, horario)

    # --- Actualizar cupo del horario ---
    horario_encontrado["cupo"] -= cantidad
    db.actualizar_cupo_por_horario(nombre_actividad, horario, horario_encontrado["cupo"])

    # --- Retornar resultado ---
    return {
        "actividad": nombre_actividad,
        "visitante": visitante,
        "horario": horario,
        "cantidad": cantidad
    }
