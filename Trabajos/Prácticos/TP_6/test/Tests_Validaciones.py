# tests/test_validaciones.py

import pytest
from app.Validaciones import (
    validar_cupos,
    validar_edad,
    validar_nombre,
    validar_dni,
    validar_talle,
    validar_horarios_disponibles,
    validar_horario_elegido,
    validar_terminos_y_condiciones,
    validar_seleccion_de_actividad,
    validar_que_actividad_exista
)


# 1. validar_cupos
def test_validar_cupos_exitoso():
    validar_cupos(5, 3)  # No debe lanzar excepción

def test_validar_cupos_falla():
    with pytest.raises(Exception) as error:
        validar_cupos(2, 3)
    assert "No hay suficientes cupos disponibles" in str(error.value)


# 2. validar_edad
def test_validar_edad_exitoso():
    validar_edad(25)  # No debe lanzar excepción
    
def test_validar_edad_falla_none():
    with pytest.raises(Exception) as error:
        validar_edad(None)
    assert "La edad es obligatoria" in str(error.value)
def test_validar_edad_falla():
    with pytest.raises(Exception) as error:
        validar_edad(0)
    assert "La edad debe ser mayor a 0" in str(error.value)
def test_validar_edad_falla_no_numerica():
    with pytest.raises(Exception) as error:
        validar_edad("veinte")
    assert "La edad debe ser un número entero" in str(error.value)
def test_validar_edad_falla_mayor_120():
    with pytest.raises(Exception) as error:
        validar_edad(130)
    assert "La edad debe ser menor a 120 años" in str(error.value)


# 3. validar_nombre
def test_validar_nombre_exitoso():
    validar_nombre("Ana")  # No debe lanzar excepción

def test_validar_nombre_falla_vacio():
    with pytest.raises(Exception) as error:
        validar_nombre("")
    assert "El nombre no puede estar vacío" in str(error.value)
def test_validar_nombre_falla_menos_de_dos_caracteres():
    with pytest.raises(Exception) as error:
        validar_nombre("A")
    assert "El nombre debe tener al menos 2 caracteres" in str(error.value)
def test_validar_nombre_falla_caracteres_invalidos():
    with pytest.raises(Exception) as error:
        validar_nombre("Ana123")
    assert "El nombre solo puede contener letras y espacios" in str(error.value)


# 4. validar_dni
def test_validar_dni_exitoso():
    validar_dni("12345678")  # No debe lanzar excepción

def test_validar_dni_falla():
    with pytest.raises(Exception) as error:
        validar_dni("")
    assert "El DNI no puede estar vacío" in str(error.value)
def test_validar_dni_falla_longitud():
    with pytest.raises(Exception) as error:
        validar_dni("1234")
    assert "El DNI debe tener entre 7 y 8 dígitos" in str(error.value)
def test_validar_dni_falla_no_numerico():
    with pytest.raises(Exception) as error:
        validar_dni("12A45678")
    assert "El DNI solo puede contener números" in str(error.value)


# 5. validar_talle
def test_validar_talle_exitoso():
    visitante = {"talle": "M"}
    validar_talle(visitante)  # No debe lanzar excepción

def test_validar_talle_falla():
    visitante = {}
    with pytest.raises(Exception) as error:
        validar_talle(visitante)
    assert "Debe ingresar el talle de vestimenta requerido por la actividad" in str(error.value)


# 6. validar_horarios_disponibles
def test_validar_horarios_disponibles_exitoso():
    horarios = [{"hora": "10:00", "cupo": 5}]
    validar_horarios_disponibles(horarios)  # No debe lanzar excepción

def test_validar_horarios_disponibles_falla():
    with pytest.raises(Exception) as error:
        validar_horarios_disponibles([])
    assert "No hay horarios disponibles" in str(error.value)


# 7. validar_horario_elegido
def test_validar_horario_elegido_exitoso():
    horarios = [{"hora": "10:00", "cupo": 5}]
    resultado = validar_horario_elegido("10:00", horarios)
    assert resultado["hora"] == "10:00"

def test_validar_horario_elegido_falla():
    horarios = [{"hora": "10:00", "cupo": 5}]
    with pytest.raises(Exception) as error:
        validar_horario_elegido("11:00", horarios)
    assert "Horario no disponible" in str(error.value)


# 8. validar_terminos_y_condiciones
def test_validar_terminos_y_condiciones_exitoso():
    validar_terminos_y_condiciones(True)

def test_validar_terminos_y_condiciones_falla():
    with pytest.raises(Exception) as error:
        validar_terminos_y_condiciones(False)
    assert "Debe aceptar los términos y condiciones" in str(error.value)


# 9. validar_seleccion_de_actividad
def test_validar_seleccion_de_actividad_exitoso():
    validar_seleccion_de_actividad("Tirolesa")

def test_validar_seleccion_de_actividad_falla():
    with pytest.raises(Exception) as error:
        validar_seleccion_de_actividad("")
    assert "Debe seleccionar una actividad" in str(error.value)


# 10. validar_que_actividad_exista
def test_validar_que_actividad_exista_exitoso():
    actividades = {"Tirolesa": {}}
    validar_que_actividad_exista(actividades, "Tirolesa")

def test_validar_que_actividad_exista_falla():
    actividades = {"Safari": {}}
    with pytest.raises(Exception) as error:
        validar_que_actividad_exista(actividades, "Tirolesa")
    assert "La actividad seleccionada no existe" in str(error.value)
# --- FIN DE test_validaciones.py ---