# Los tests que corresponden a la user story "inscribirme a actividad" quedan almacenados todos dentro del mismo file "test_inscripcion.py" , porque los mismos pertenecen a una unica User Story.

# Se usa el framework pytest para la ejecucion de las pruebas automatizadas.
# Las mismas se ejecutan dentro de un entorno virtual (virtualenv), con el fin de mantener aisladas las dependencias necesarias para el desarrollo

# ¿Como CREAR el entorno virtual?
#   pip install virtualenv
#   pip install pytest
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  
#   python -m venv .venv

# ¿Como activo el entorno virtual?
#   .venv\Scripts\activate en Powershell
#   source .venv\Scripts\activate en gitbash

# ¿Como ejecuto las pruebas? 
#   pytest -v