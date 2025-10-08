# Los tets de la inscripción quedan almacenados todos dentro del mismo file, no vemos necesario
# hacer un file para cada test porque los mismos pertenecen a una unica User Story

# Se usa el paquete pytest para las pruebas automatizadas, dicho paquete esta instalado dentro
# un entorno virtual, creemos que es mejor organizarlo de esta forma para lograr abstraer la 
# implementacion dentro de un entorno donde sólo esten ciertos paquetes necesarios para el desarrollo

# ¿Como activo el entorno virtual?
#   pip install virtualenv
#   pip install pytest
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  
#   .venv\Scripts\activate 

# ¿Como ejecuto las pruebas? 
#   pytest -v