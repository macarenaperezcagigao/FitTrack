# db/ejercicios.py
import sqlite3

RUTA_DB = "fittrack.db"

# ═══════════════════════════════════════════════════════════════
# CREATE - CREAR EJERCICIO
# ═══════════════════════════════════════════════════════════════

def crear_ejercicio(rutina_id, nombre, series, repeticiones, descanso, notas=""):
    """Crea un nuevo ejercicio en una rutina"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO ejercicios (rutina_id, nombre, series, repeticiones, descanso, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (rutina_id, nombre, series, repeticiones, descanso, notas))
        conexion.commit()
        ejercicio_id = cursor.lastrowid
        conexion.close()
        print(f"✅ Ejercicio creado con ID {ejercicio_id}")
        return ejercicio_id
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# READ - LEER EJERCICIOS
# ═══════════════════════════════════════════════════════════════

def obtener_ejercicios(rutina_id):
    """Obtiene todos los ejercicios de una rutina"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ejercicios WHERE rutina_id = ?", (rutina_id,))
        ejercicios = cursor.fetchall()
        conexion.close()
        return [dict(ejercicio) for ejercicio in ejercicios]
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def obtener_ejercicio_por_id(ejercicio_id):
    """Obtiene un ejercicio específico"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ejercicios WHERE id = ?", (ejercicio_id,))
        ejercicio = cursor.fetchone()
        conexion.close()
        return dict(ejercicio) if ejercicio else None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# UPDATE - ACTUALIZAR EJERCICIO
# ═══════════════════════════════════════════════════════════════

def actualizar_ejercicio(ejercicio_id, nombre, series, repeticiones, descanso, notas=""):
    """Actualiza un ejercicio existente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE ejercicios 
            SET nombre=?, series=?, repeticiones=?, descanso=?, notas=?
            WHERE id = ?
        """, (nombre, series, repeticiones, descanso, notas, ejercicio_id))
        conexion.commit()
        conexion.close()
        print(f"✅ Ejercicio {ejercicio_id} actualizado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# DELETE - ELIMINAR EJERCICIO
# ═══════════════════════════════════════════════════════════════

def eliminar_ejercicio(ejercicio_id):
    """Elimina un ejercicio"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM ejercicios WHERE id = ?", (ejercicio_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Ejercicio {ejercicio_id} eliminado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False