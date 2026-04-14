# db/database.py
# Inicialización de base de datos

import sqlite3
from config.settings import RUTA_DB

def crear_tablas():
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
            notas TEXT
        )
    """)
    
    conexion.commit()
    conexion.close()
    print("✅ Base de datos iniciada")