# db/sesiones.py
import sqlite3

RUTA_DB = "fittrack.db"

# ═══════════════════════════════════════════════════════════════
# CREATE - CREAR SESIÓN
# ═══════════════════════════════════════════════════════════════

def crear_sesion(cliente_id, duracion, tipo, valoracion, notas=""):
    """Registra una nueva sesión de entrenamiento"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO sesiones (cliente_id, duracion, tipo, valoracion, notas)
            VALUES (?, ?, ?, ?, ?)
        """, (cliente_id, duracion, tipo, valoracion, notas))
        conexion.commit()
        sesion_id = cursor.lastrowid
        conexion.close()
        print(f"✅ Sesión creada con ID {sesion_id}")
        return sesion_id
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# READ - LEER SESIONES
# ═══════════════════════════════════════════════════════════════

def obtener_sesiones(cliente_id):
    """Obtiene todas las sesiones de un cliente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM sesiones WHERE cliente_id = ? ORDER BY fecha DESC", (cliente_id,))
        sesiones = cursor.fetchall()
        conexion.close()
        return [dict(sesion) for sesion in sesiones]
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def obtener_sesion_por_id(sesion_id):
    """Obtiene una sesión específica"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM sesiones WHERE id = ?", (sesion_id,))
        sesion = cursor.fetchone()
        conexion.close()
        return dict(sesion) if sesion else None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# UPDATE - ACTUALIZAR SESIÓN
# ═══════════════════════════════════════════════════════════════

def actualizar_sesion(sesion_id, duracion, tipo, valoracion, notas=""):
    """Actualiza una sesión existente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE sesiones 
            SET duracion=?, tipo=?, valoracion=?, notas=?
            WHERE id = ?
        """, (duracion, tipo, valoracion, notas, sesion_id))
        conexion.commit()
        conexion.close()
        print(f"✅ Sesión {sesion_id} actualizada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# DELETE - ELIMINAR SESIÓN
# ═══════════════════════════════════════════════════════════════

def eliminar_sesion(sesion_id):
    """Elimina una sesión"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM sesiones WHERE id = ?", (sesion_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Sesión {sesion_id} eliminada")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False