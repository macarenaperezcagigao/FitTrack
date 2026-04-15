# db/database.py
import sqlite3
from datetime import datetime

RUTA_DB = "fittrack.db"

def crear_tablas():
    """Crea todas las tablas de la BD si no existen"""
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            edad INTEGER,
            email TEXT,
            telefono TEXT,
            genero TEXT,
            peso REAL,
            altura REAL,
            grasa_corporal REAL,
            objetivo TEXT,
            notas TEXT,
            activo INTEGER DEFAULT 1,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progreso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            peso REAL,
            grasa_corporal REAL,
            pecho REAL,
            cintura REAL,
            cadera REAL,
            brazos REAL,
            piernas REAL,
            hombros REAL,
            notas TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rutinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            dias TEXT,
            descripcion TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ejercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rutina_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            series INTEGER,
            repeticiones INTEGER,
            descanso INTEGER,
            notas TEXT,
            FOREIGN KEY (rutina_id) REFERENCES rutinas(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duracion INTEGER,
            tipo TEXT,
            valoracion INTEGER,
            notas TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    
    conexion.commit()
    conexion.close()
    print("✅ Tablas creadas correctamente")