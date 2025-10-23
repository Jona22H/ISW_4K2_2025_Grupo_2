import sqlite3

DB_FILE = "Eco_Harmony.db"

def crear_tablas():
    """Crea las tablas de actividades, horarios y participantes si no existen"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Tabla de actividades (solo info general)
    c.execute("""
        CREATE TABLE IF NOT EXISTS actividades (
            nombre TEXT PRIMARY KEY,
            requiere_talle INTEGER NOT NULL,
            terminos TEXT
        )
    """)

    # Tabla de horarios con cupos por horario
    c.execute("""
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actividad TEXT NOT NULL,
            horario TEXT NOT NULL,
            cupo INTEGER NOT NULL,
            FOREIGN KEY(actividad) REFERENCES actividades(nombre),
            UNIQUE(actividad, horario)
        )
    """)

    # Tabla de participantes
    c.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni INTEGER NOT NULL,
            edad INTEGER NOT NULL,
            talle TEXT,
            actividad TEXT NOT NULL,
            horario TEXT NOT NULL,
            FOREIGN KEY(actividad) REFERENCES actividades(nombre)
        )
    """)

    conn.commit()
    conn.close()

def inicializar_actividades():
    """Agrega las actividades iniciales con sus horarios y cupos específicos si no existen"""
    actividades = {
        "Tirolesa": {
            "requiere_talle": True,
            "horarios": [
                {"hora": "10:00", "cupo": 5},
                {"hora": "14:00", "cupo": 8}
            ],
            "terminos": "- Uso obligatorio del arnés y casco\n- No se permite exceder el peso máximo\n- Horario estricto"
        },
        "Safari": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "11:00", "cupo": 3},
                {"hora": "15:00", "cupo": 3}
            ],
            "terminos": "- Seguir al guía en todo momento\n- No alimentar animales\n- Horario estricto"
        },
        "Palestra": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "09:00", "cupo": 4},
                {"hora": "13:00", "cupo": 2}
            ],
            "terminos": "- Traer ropa cómoda\n- Horario estricto"
        },
        "Jardinería": {
            "requiere_talle": False,
            "horarios": [
                {"hora": "10:00", "cupo": 6},
                {"hora": "14:00", "cupo": 4}
            ],
            "terminos": "- Traer guantes\n- No arrancar plantas sin permiso\n- Horario estricto"
        }
    }

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    for nombre, info in actividades.items():
        # Insertar actividad si no existe
        c.execute("""
            INSERT OR IGNORE INTO actividades (nombre, requiere_talle, terminos)
            VALUES (?, ?, ?)
        """, (nombre, int(info["requiere_talle"]),info["terminos"]))

        # Insertar horarios con sus cupos individuales
        for h in info["horarios"]:
            c.execute("""
                INSERT OR IGNORE INTO horarios (actividad, horario, cupo)
                VALUES (?, ?, ?)
            """, (nombre, h["hora"], h["cupo"]))

    conn.commit()
    conn.close()

# Global connection for transaction management
conn = None

def start_transaction():
    """Inicia una transacción y devuelve la conexión"""
    global conn
    conn = sqlite3.connect(DB_FILE)
    conn.execute("BEGIN TRANSACTION")
    return conn

def guardar_participante(participante, actividad, horario):
    """Guarda un participante en la base de datos"""
    global conn
    c = conn.cursor()
    c.execute("""
        INSERT INTO participantes (nombre, dni, edad, talle, actividad, horario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        participante["nombre"],
        participante["dni"],
        participante["edad"],
        participante.get("talle"),
        actividad,
        horario
    ))


def actualizar_cupo_por_horario(actividad, horario, nuevo_cupo):
    """Actualiza el cupo disponible para un horario específico de una actividad"""
    global conn
    c = conn.cursor()
    c.execute("""
        UPDATE horarios
        SET cupo = ?
        WHERE actividad = ? AND horario = ?
    """, (nuevo_cupo, actividad, horario))


def obtener_actividades():
    """Devuelve todas las actividades con sus horarios y cupos"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT a.nombre, a.requiere_talle, a.terminos, h.horario, h.cupo
        FROM actividades a
        JOIN horarios h ON a.nombre = h.actividad
    """)
    rows = c.fetchall()
    conn.close()

    actividades = {}
    for nombre, requiere_talle, terminos, horario, cupo in rows:
        if nombre not in actividades:
            actividades[nombre] = {
                "requiere_talle": bool(requiere_talle),
                "terminos": terminos,
                "horarios": []
            }
        actividades[nombre]["horarios"].append({
            "hora": horario,
            "cupo": cupo
        })

    return actividades

def commit():
    """Realiza un commit de la base de datos"""
    global conn
    conn.commit()
    conn.close()
    conn = None

def rollback():
    """Realiza un rollback de la base de datos en caso de error"""
    global conn
    if conn:
        conn.rollback()
    conn.close()
