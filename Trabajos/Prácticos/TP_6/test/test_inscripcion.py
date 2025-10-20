# tests/test_inscripcion.py

from app.inscripcion import inscribirse_a_actividad
import pytest

# PRIMER PRUEBA: Inscribirse a una actividad del listado que poseen cupos disponibles, seleccionando un horario, 
# ingresando los datos del visitante (nombre, DNI, edad, talla de la vestimenta si la actividad lo requiere) y aceptando 
# los términos y condiciones (pasa)

def test_inscripcion_exitosa():
    # --- PRECONDICIONES ---
    actividades = {
        "Tirolesa": {"cupo": 5, 
                     "requiere_talle": True,
                     "horarios_disponibles": ["10:00", "14:00"]}
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
        horario=horario_seleccionado
    )

    # --- RESULTADOS ---
    assert resultado["actividad"] == "Tirolesa", "No se inscribió correctamente"
    assert actividades["Tirolesa"]["cupo"] == 4, "No se redujo el cupo correctamente"

    print("✅ La inscripción se realizó correctamente.")

# SEGUNDA PRUEBA: Inscribirse a una actividad que no tiene cupo para el horario seleccionado (falla)

def test_inscripcion_falla_sin_cupos():
    # --- PRECONDICIONES ---
    actividades = {
        "Safari": {"cupo": 0,
                   "requiere_talle": False,
                   "horarios_disponibles": ["11:00", "15:00"]}
    }

    visitante = {
        "nombre": "Pedro",
        "dni": "87654321",
        "edad": 25
    }

    horario_seleccionado = "11:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    # Intentamos inscribir cuando no hay cupos
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Safari",
            visitante=visitante,
            terminos_aceptados=True,
            horario=horario_seleccionado
        )

    # --- RESULTADOS ---
    assert "No hay cupos disponibles" in str(error.value), "El mensaje de error no es correcto"
    print("✅ La prueba falló correctamente cuando no había cupos disponibles.")

# TERCER PRUEBA: Inscribirse a una actividad sin ingresar talle de vestimenta porque la actividad no lo requiere (pasa)

def test_inscripcion_exitosa_sin_talle():
    # --- PRECONDICIONES ---
    actividades = {
        "Safari": {"cupo": 3,
                   "requiere_talle": False,
                   "horarios_disponibles": ["11:00", "15:00"]}
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
        horario=horario_seleccionado
    )

    # --- RESULTADOS ---
    assert resultado["actividad"] == "Safari", "No se inscribió correctamente"
    assert actividades["Safari"]["cupo"] == 2, "No se redujo el cupo correctamente"
    print("✅ La inscripción se realizó correctamente sin requerir talle.")

# CUARTA PRUEBA: Inscribirse a una actividad seleccionando un horario en el cual el parque está cerrado o la actividad no está disponible (falla)

def test_inscripcion_falla_horario_cerrado():
    # --- PRECONDICIONES ---
    actividades = {
        "Jardinería": {
            "cupo": 5,
            "requiere_talle": False,
            "horarios_disponibles": ["10:00", "14:00"]  # horarios en los que la actividad está abierta
        }
    }

    visitante = {
        "nombre": "Luciano",
        "dni": "55667788",
        "edad": 30
    }

    horario_seleccionado = "12:00"  # horario en el que la actividad no está disponible

    # --- PASOS DEL CASO DE PRUEBA ---
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Jardinería",
            visitante=visitante,
            terminos_aceptados=True,
            horario=horario_seleccionado  # suponiendo que la función acepta este parámetro
        )

    # --- RESULTADOS ---
    assert "Horario no disponible" in str(error.value), "El mensaje de error no es correcto"
    print("✅ La prueba falló correctamente porque el horario seleccionado no estaba disponible.")

# QUINTA PRUEBA: Inscribirse a una actividad sin aceptar los términos y condiciones de la actividad (falla)

def test_inscripcion_falla_sin_aceptar_terminos():
    # --- PRECONDICIONES ---
    actividades = {
        "Palestra": {"cupo": 3,
                     "requiere_talle": False,
                     "horarios_disponibles": ["09:00", "13:00"]}
    }

    visitante = {
        "nombre": "Lucía",
        "dni": "11223344",
        "edad": 27
    }

    horario_seleccionado = "09:00"

    # --- PASOS DEL CASO DE PRUEBA ---
    # Intentamos inscribir sin aceptar los términos
    
    with pytest.raises(Exception) as error:
        inscribirse_a_actividad(
            actividades=actividades,
            nombre_actividad="Palestra",
            visitante=visitante,
            terminos_aceptados=False,
            horario=horario_seleccionado
        )

    # --- RESULTADOS ---
    assert "Debe aceptar los términos y condiciones" in str(error.value), "El mensaje de error no es correcto"
    print("✅ La prueba falló correctamente cuando no se aceptaron los términos y condiciones.")

# SEXTA PRUEBA: No se ingresa el talle cuando la actividad lo requiere (falla)

def test_inscripcion_falla_sin_talle_requerido():
    # --- PRECONDICIONES ---
    actividades = {
        "Tirolesa": {"cupo": 5,
                     "requiere_talle": True,
                     "horarios_disponibles": ["10:00", "14:00"]}
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
            horario=horario_seleccionado
        )

    # --- RESULTADOS ---
    assert "Debe ingresar el talle de vestimenta requerido por la actividad" in str(error.value), "El mensaje de error no es correcto"
    print("✅ La prueba falló correctamente porque no se ingresó el talle requerido.")
