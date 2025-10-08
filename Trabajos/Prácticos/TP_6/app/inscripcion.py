# app/inscripcion.py

def inscribirse_a_actividad(actividades, nombre_actividad, visitante, terminos_aceptados, horario):
    """
    Permite a un visitante inscribirse en una actividad si hay cupos y acepta los términos.
    Valida talle si la actividad lo requiere y verifica que el horario seleccionado esté disponible.
    """
    if not terminos_aceptados:
        raise Exception("Debe aceptar los términos y condiciones")

    actividad = actividades[nombre_actividad]

    if actividad["cupo"] <= 0:
        raise Exception("No hay cupos disponibles")

    # Validar talle si se requiere
    if actividad.get("requiere_talle", False):
        if "talle" not in visitante or not visitante["talle"]:
            raise Exception("Debe ingresar el talle de vestimenta requerido por la actividad")

    # Validar horario
    horarios_disponibles = actividad.get("horarios_disponibles")
    if not horarios_disponibles or horario not in horarios_disponibles:
        raise Exception("Horario no disponible")

    # Reducir el cupo
    actividad["cupo"] -= 1

    # Devolver información de la inscripción
    return {
        "actividad": nombre_actividad,
        "visitante": visitante,
        "horario": horario
    }


