# db/progreso.py
import sqlite3
from datetime import datetime

RUTA_DB = "fittrack.db"

# ═══════════════════════════════════════════════════════════════
# CREATE - CREAR REGISTRO DE PROGRESO
# ═══════════════════════════════════════════════════════════════

def crear_progreso(cliente_id, peso, grasa, pecho, cintura, cadera, brazos, piernas, hombros, notas=""):
    """Registra un nuevo progreso para un cliente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO progreso (cliente_id, peso, grasa_corporal, pecho, cintura, cadera, brazos, piernas, hombros, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cliente_id, peso, grasa, pecho, cintura, cadera, brazos, piernas, hombros, notas))
        conexion.commit()
        conexion.close()
        print(f"✅ Progreso registrado para cliente {cliente_id}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# READ - LEER REGISTROS DE PROGRESO
# ═══════════════════════════════════════════════════════════════

def obtener_progreso(cliente_id):
    """Obtiene todos los registros de progreso de un cliente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM progreso WHERE cliente_id = ? ORDER BY fecha DESC", (cliente_id,))
        registros = cursor.fetchall()
        conexion.close()
        return [dict(registro) for registro in registros]
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def obtener_progreso_por_id(progreso_id):
    """Obtiene un registro específico de progreso"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM progreso WHERE id = ?", (progreso_id,))
        registro = cursor.fetchone()
        conexion.close()
        return dict(registro) if registro else None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# UPDATE - ACTUALIZAR REGISTRO DE PROGRESO
# ═══════════════════════════════════════════════════════════════

def actualizar_progreso(progreso_id, peso, grasa, pecho, cintura, cadera, brazos, piernas, hombros, notas=""):
    """Actualiza un registro de progreso existente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE progreso 
            SET peso=?, grasa_corporal=?, pecho=?, cintura=?, cadera=?, brazos=?, piernas=?, hombros=?, notas=?
            WHERE id = ?
        """, (peso, grasa, pecho, cintura, cadera, brazos, piernas, hombros, notas, progreso_id))
        conexion.commit()
        conexion.close()
        print(f"✅ Progreso {progreso_id} actualizado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# DELETE - ELIMINAR REGISTRO DE PROGRESO
# ═══════════════════════════════════════════════════════════════

def eliminar_progreso(progreso_id):
    """Elimina un registro de progreso"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM progreso WHERE id = ?", (progreso_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Progreso {progreso_id} eliminado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False