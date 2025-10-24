# TP_6 - Sistema de Inscripción a Actividades


Los tests correspondientes a la user story "inscribirme a actividad" están almacenados en el archivo `Test_Inscripcion.py`, ya que pertenecen a una única User Story.

## Tecnologías Utilizadas

- **Framework de Testing**: `pytest` para la ejecución de pruebas automatizadas
- **Entorno Virtual**: `virtualenv` para mantener aisladas las dependencias
- **Frontend**: `streamlit` para una interfaz simple y funcional

## Configuración del Entorno

### 1. Crear el entorno virtual

```bash
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 2. Activar el entorno virtual

**En PowerShell:**
```powershell
.venv/Scripts/activate
```

**En Git Bash:**
```bash
source .venv/Scripts/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```
> Agregar la flag `--user` si no deja por permisos

## Ejecutar las Pruebas

```bash
pytest -v nombredelarchivoconlostests.py
```

## Levantar la Aplicación

```bash
streamlit run main.py
```
