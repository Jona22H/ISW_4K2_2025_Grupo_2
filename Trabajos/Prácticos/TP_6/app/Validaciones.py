# app/validaciones.py
import re
import streamlit as st

def validar_nombre(nombre):
    """
    Valida que el nombre tenga formato correcto y no esté vacío.
    
    Args:
        nombre (str): El nombre completo a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
               - es_valido: True si el nombre es válido, False en caso contrario
               - mensaje_error: Descripción del error si es_valido es False, cadena vacía si es válido
    """
    if not nombre or nombre.strip() == "":
        raise Exception("El nombre no puede estar vacío")
    if len(nombre.strip()) < 2:
        raise Exception("El nombre debe tener al menos 2 caracteres")
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre.strip()):
        raise Exception("El nombre solo puede contener letras y espacios")
    return True, ""

def validar_edad(edad):
    """
    Valida que la edad esté dentro del rango permitido.
    
    Args:
        edad (int): La edad a validar
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
               - es_valido: True si la edad es válida, False en caso contrario
               - mensaje_error: Descripción del error si es_valido es False, cadena vacía si es válido
    """
    if edad is None:
        raise Exception("La edad es obligatoria")
    if not isinstance(edad, int):
        raise Exception("La edad debe ser un número entero")
    if edad is None or edad <= 0:
        raise Exception("La edad debe ser mayor a 0")
    if edad > 120:
        raise Exception("La edad debe ser menor a 120 años")
    return True, ""

def validar_dni(dni):
    """
    Valida que el DNI tenga formato y longitud correctos.
    
    Args:
        dni (str): El DNI a validar (puede contener puntos y espacios)
        
    Returns:
        tuple: (bool, str) - (es_valido, mensaje_error)
               - es_valido: True si el DNI es válido, False en caso contrario
               - mensaje_error: Descripción del error si es_valido es False, cadena vacía si es válido
    """
    if not dni or dni.strip() == "":
        raise Exception("El DNI no puede estar vacío")
    # Remover puntos y espacios
    dni_limpio = re.sub(r'[.\s]', '', dni.strip())
    if not dni_limpio.isdigit():
        raise Exception("El DNI solo puede contener números")
    if len(dni_limpio) < 7 or len(dni_limpio) > 8:
        raise Exception("El DNI debe tener entre 7 y 8 dígitos")
    return True, ""

def validar_talle(visitante):
    """
    Valida que el talle esté presente en el diccionario del visitante.
    
    Args:
        visitante (dict): Diccionario con los datos del visitante
        
    Raises:
        Exception: Si el talle no está presente o es inválido
    """
    if "talle" not in visitante or not visitante["talle"]:
        raise Exception("Debe ingresar el talle de vestimenta requerido por la actividad")
    
    talles_permitidos = ["XS", "S", "M", "L", "XL", "XXL"]
    if visitante["talle"] not in talles_permitidos:
        raise Exception("El talle ingresado no es válido")

def validar_terminos_y_condiciones(terminos_aceptados):
    """
    Valida que los términos y condiciones hayan sido aceptados.
    
    Args:
        terminos_aceptados (bool): Indica si se aceptaron los términos
        
    Raises:
        Exception: Si los términos no fueron aceptados
    """
    if not terminos_aceptados:
        raise Exception("Debe aceptar los términos y condiciones")

def validar_horarios_disponibles(horarios_disponibles):
    """
    Valida que la lista de horarios no esté vacía.
    
    Args:
        horarios (list): Lista de horarios disponibles
        
    Raises:
        Exception: Si la lista de horarios está vacía
    """
    if not horarios_disponibles or len(horarios_disponibles) == 0:
        raise Exception("No hay horarios disponibles para la actividad seleccionada")
    
def validar_horario_elegido(horario_elegido, horarios_disponibles):
    """
    Valida que el horario elegido esté dentro de los horarios disponibles.

    Args:
        horario_elegido (str): Horario seleccionado por el usuario
        horarios_disponibles (list): Lista de horarios disponibles para la actividad
    Returns:
        dict: El horario encontrado dentro de los horarios disponibles
    Raises:
        Exception: Si el horario elegido no está disponible
    """
    horario_encontrado = None
    encontrado = False
    for h in horarios_disponibles:
        if h["hora"] == horario_elegido:
            encontrado = True
            horario_encontrado = h
            break
    if not encontrado:
        raise Exception("Horario no disponible")
    return horario_encontrado

def validar_cupos(cupo_disponible, cantidad_solicitada):
    """
    Valida que haya suficientes cupos disponibles para la cantidad solicitada.
    
    Args:
        cupo_disponible (int): Cupo disponible en el horario seleccionado
        cantidad_solicitada (int): Cantidad de participantes que se desean inscribir
        
    Raises:
        Exception: Si no hay suficientes cupos disponibles
    """
    if cupo_disponible < cantidad_solicitada:
        raise Exception("No hay suficientes cupos disponibles para la cantidad de participantes solicitada")

def validar_seleccion_de_actividad(nombre_actividad):
    """
    Valida que se haya seleccionado una actividad.
    
    Args:
        nombre_actividad (str): Nombre de la actividad seleccionada
        
    Raises:
        Exception: Si no se ha seleccionado ninguna actividad
    """
    if not nombre_actividad or nombre_actividad.strip() == "":
        raise Exception("Debe seleccionar una actividad")
    
def validar_que_actividad_exista(actividades, nombre_actividad):
    """
    Valida que la actividad seleccionada exista en la lista de actividades.
    
    Args:
        actividades (dict): Diccionario de actividades disponibles
        nombre_actividad (str): Nombre de la actividad seleccionada
        
    Raises:
        Exception: Si la actividad no existe
    """
    if nombre_actividad not in actividades:
        raise Exception("La actividad seleccionada no existe")