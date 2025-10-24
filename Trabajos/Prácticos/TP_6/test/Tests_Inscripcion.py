# tests/test_inscripcion.py

from app.Inscripcion import inscribirse_a_actividad
import pytest
from app.DB import start_transaction, commit

@pytest.fixture(autouse=True)
def setup_db():
    start_transaction()
    yield
    commit()

# PRIMER PRUEBA: Inscribirse a una actividad del listado que poseen cupos disponibles, seleccionando un horario, 
# ingresando los datos del visitante (nombre, DNI, edad, talla de la vestimenta si la actividad lo requiere) y aceptando 
# los términos y condiciones (pasa)

def test_inscripcion_exitosa():
    # --- PRECONDICIONES ---
    actividades = {
        "Tirolesa": {
            "requiere_talle": True,
            "horarios": [
                {"hora": "10:00", "cupo": 5},
                {"hora": "14:00", "cupo": 5}
            ],
            "terminos": "- Uso obligatorio del arnés y casco\n- No se permite exceder el peso máximo\n- Horario estricto"
        }
    }

    visitante = {
        "nombre": "Ana",
        "dni": "12345678",
        "edad": 30,
        "talle": "M"
    }

    horario_seleccionado = "10:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    resultado = inscribirse_a_actividad(
        actividades=actividades,
        nombre_actividad="Tirolesa",
        visitante=visitante,
        terminos_aceptados=True,
        horario=horario_seleccionado,
        cantidad=1,
    )

    # --- RESULTADOS ---
    assert resultado["actividad"] == "Tirolesa", "No se inscribió correctamente"

    # Verificar que el cupo del horario 10:00 se haya reducido
    for h in actividades["Tirolesa"]["horarios"]:
        if h["hora"] == horario_seleccionado:
            assert h["cupo"] == 4, "No se redujo el cupo correctamente"
            break
    else:
        raise AssertionError("Horario seleccionado no encontrado en la actividad")


# SEGUNDA PRUEBA: Inscribirse a una actividad que no tiene cupo para el horario seleccionado (falla)
def test_inscripcion_falla_sin_cupos():
    # --- PRECONDICIONES ---
    actividades = {
        "Safari": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "11:00", "cupo": 0},
                {"hora": "15:00", "cupo": 3}
            ],
            "terminos": "- Seguir al guía en todo momento\n- No alimentar animales\n- Horario estricto"
        }
    }

    visitante = {
        "nombre": "Pedro",
        "dni": "87654321",
        "edad": 25
    }

    horario_seleccionado = "11:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Safari",
            visitante=visitante,
            terminos_aceptados=True,
            horario=horario_seleccionado,
            cantidad=1
        )

    # --- RESULTADOS ---
    assert "No hay suficientes cupos disponibles" in str(error.value), "El mensaje de error no es correcto"

# TERCER PRUEBA: Inscribirse a una actividad sin ingresar talle de vestimenta porque la actividad no lo requiere (pasa)
def test_inscripcion_exitosa_sin_talle():
    # --- PRECONDICIONES ---
    actividades = {
        "Safari": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "11:00", "cupo": 3},
                {"hora": "15:00", "cupo": 3}
            ],
            "terminos": "- Seguir al guía en todo momento\n- No alimentar animales\n- Horario estricto"
        }
    }

    visitante = {
        "nombre": "Pedro",
        "dni": "87654321",
        "edad": 25
        # No se incluye 'talle' porque no se requiere
    }

    horario_seleccionado = "11:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    resultado = inscribirse_a_actividad(
        actividades=actividades,
        nombre_actividad="Safari",
        visitante=visitante,
        terminos_aceptados=True,
        horario=horario_seleccionado,
        cantidad=1
    )

    # --- RESULTADOS ---
    assert resultado["actividad"] == "Safari", "No se inscribió correctamente"
    # Reducir cupo del horario seleccionado
    cupo_horario = next(h for h in actividades["Safari"]["horarios"] if h["hora"] == horario_seleccionado)
    assert cupo_horario["cupo"] == 2, "No se redujo el cupo correctamente"

# CUARTA PRUEBA: Inscribirse a una actividad en horario no disponible (falla)
def test_inscripcion_falla_horario_cerrado():
    # --- PRECONDICIONES ---
    actividades = {
        "Jardinería": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "10:00", "cupo": 5},
                {"hora": "14:00", "cupo": 5}
            ],
            "terminos": "- Traer guantes\n- No arrancar plantas sin permiso\n- Horario estricto"
        }
    }

    visitante = {
        "nombre": "Luciano",
        "dni": "55667788",
        "edad": 30
    }

    horario_seleccionado = "12:00"  # horario no disponible

    # --- PASOS DEL CASO DE PRUEBA ---
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Jardinería",
            visitante=visitante,
            terminos_aceptados=True,
            horario=horario_seleccionado,
            cantidad=1
        )

    # --- RESULTADOS ---
    assert "Horario no disponible" in str(error.value), "El mensaje de error no es correcto"

# QUINTA PRUEBA: Inscribirse a una actividad sin aceptar los términos y condiciones de la actividad (falla)

def test_inscripcion_falla_sin_aceptar_terminos():
    # --- PRECONDICIONES ---
    actividades = {
        "Palestra": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "09:00", "cupo": 3},
                {"hora": "13:00", "cupo": 3}
            ],
            "terminos": "- Traer ropa cómoda\n- Horario estricto"
        }
    }

    visitante = {
        "nombre": "Lucía",
        "dni": "11223344",
        "edad": 27
    }

    horario_seleccionado = "09:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Palestra",
            visitante=visitante,
            terminos_aceptados=False,
            horario=horario_seleccionado,
            cantidad=1
        )

    # --- RESULTADOS ---
    assert "Debe aceptar los términos y condiciones" in str(error.value), "El mensaje de error no es correcto"

# SEXTA PRUEBA: Inscribirse a una actividad que requiere talle de vestimenta sin ingresar dicho dato (falla)

def test_inscripcion_falla_sin_talle_requerido():
    # --- PRECONDICIONES ---
    actividades = {
        "Tirolesa": {
            "requiere_talle": True,
            "horarios": [
                {"hora": "10:00", "cupo": 5},
                {"hora": "14:00", "cupo": 5}
            ],
            "terminos": "- Uso obligatorio del arnés y casco\n- No se permite exceder el peso máximo\n- Horario estricto"
        }
    }

    visitante = {
        "nombre": "Ana",
        "dni": "12345678",
        "edad": 30
        # No se incluye 'talle', aunque la actividad lo requiere
    }

    horario_seleccionado = "10:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Tirolesa",
            visitante=visitante,
            terminos_aceptados=True,
            horario=horario_seleccionado,
            cantidad=1
        )

    # --- RESULTADOS ---
    assert "Debe ingresar el talle de vestimenta requerido por la actividad" in str(error.value), "El mensaje de error no es correcto"
