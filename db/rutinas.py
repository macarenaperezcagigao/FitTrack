# db/rutinas.py
import sqlite3

RUTA_DB = "fittrack.db"

# ═══════════════════════════════════════════════════════════════
# CREATE - CREAR RUTINA
# ═══════════════════════════════════════════════════════════════

def crear_rutina(cliente_id, nombre, dias, descripcion=""):
    """Crea una nueva rutina de entrenamiento"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO rutinas (cliente_id, nombre, dias, descripcion)
            VALUES (?, ?, ?, ?)
        """, (cliente_id, nombre, dias, descripcion))
        conexion.commit()
        rutina_id = cursor.lastrowid
        conexion.close()
        print(f"✅ Rutina creada con ID {rutina_id}")
        return rutina_id
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# READ - LEER RUTINAS
# ═══════════════════════════════════════════════════════════════

def obtener_rutinas(cliente_id):
    """Obtiene todas las rutinas de un cliente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM rutinas WHERE cliente_id = ? ORDER BY fecha_creacion DESC", (cliente_id,))
        rutinas = cursor.fetchall()
        conexion.close()
        return [dict(rutina) for rutina in rutinas]
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def obtener_rutina_por_id(rutina_id):
    """Obtiene una rutina específica"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM rutinas WHERE id = ?", (rutina_id,))
        rutina = cursor.fetchone()
        conexion.close()
        return dict(rutina) if rutina else None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# UPDATE - ACTUALIZAR RUTINA
# ═══════════════════════════════════════════════════════════════

def actualizar_rutina(rutina_id, nombre, dias, descripcion=""):
    """Actualiza una rutina existente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE rutinas 
            SET nombre=?, dias=?, descripcion=?
            WHERE id = ?
        """, (nombre, dias, descripcion, rutina_id))
        conexion.commit()
        conexion.close()
        print(f"✅ Rutina {rutina_id} actualizada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# DELETE - ELIMINAR RUTINA
# ═══════════════════════════════════════════════════════════════

def eliminar_rutina(rutina_id):
    """Elimina una rutina (y sus ejercicios asociados)"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM rutinas WHERE id = ?", (rutina_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Rutina {rutina_id} eliminada (ejercicios también)")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False