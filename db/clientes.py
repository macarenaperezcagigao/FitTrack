# db/clientes.py
import sqlite3

def crear_cliente(nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas):
    """Crea un nuevo cliente"""
    try:
        conexion = sqlite3.connect("fittrack.db")
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente '{nombre}' creado")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ El cliente '{nombre}' ya existe")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def obtener_clientes(busqueda="", solo_activos=True):
    """Obtiene clientes (activos por defecto)"""
    conexion = sqlite3.connect("fittrack.db")
    cursor = conexion.cursor()
    
    if busqueda:
        query = "SELECT * FROM clientes WHERE nombre LIKE ? AND activo = ?"
        cursor.execute(query, (f"%{busqueda}%", 1 if solo_activos else 0))
    else:
        query = "SELECT * FROM clientes WHERE activo = ?"
        cursor.execute(query, (1 if solo_activos else 0,))
    
    clientes = cursor.fetchall()
    conexion.close()
    
    return [
        {
            'id': c[0], 'nombre': c[1], 'edad': c[2], 'email': c[3],
            'telefono': c[4], 'genero': c[5], 'peso': c[6], 'altura': c[7],
            'grasa_corporal': c[8], 'objetivo': c[9], 'notas': c[10],
            'activo': c[11], 'fecha_registro': c[12]
        }
        for c in clientes
    ]

def obtener_cliente(cliente_id):
    """Obtiene un cliente específico"""
    conexion = sqlite3.connect("fittrack.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conexion.close()
    
    if cliente:
        return {
            'id': cliente[0], 'nombre': cliente[1], 'edad': cliente[2], 'email': cliente[3],
            'telefono': cliente[4], 'genero': cliente[5], 'peso': cliente[6], 'altura': cliente[7],
            'grasa_corporal': cliente[8], 'objetivo': cliente[9], 'notas': cliente[10],
            'activo': cliente[11], 'fecha_registro': cliente[12]
        }
    return None

def actualizar_cliente(cliente_id, nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas):
    """Actualiza datos de un cliente"""
    try:
        conexion = sqlite3.connect("fittrack.db")
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET nombre = ?, edad = ?, email = ?, telefono = ?, genero = ?, 
                peso = ?, altura = ?, grasa_corporal = ?, objetivo = ?, notas = ?
            WHERE id = ?
        """, (nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas, cliente_id))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente {cliente_id} actualizado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def eliminar_cliente(cliente_id):
    """Elimina un cliente (RGPD - eliminación completa)"""
    try:
        conexion = sqlite3.connect("fittrack.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente {cliente_id} eliminado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def desactivar_cliente(cliente_id):
    """Marca cliente como inactivo (pausa)"""
    try:
        conexion = sqlite3.connect("fittrack.db")
        cursor = conexion.cursor()
        cursor.execute("UPDATE clientes SET activo = 0 WHERE id = ?", (cliente_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente {cliente_id} desactivado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def reactivar_cliente(cliente_id):
    """Marca cliente como activo (reactiva)"""
    try:
        conexion = sqlite3.connect("fittrack.db")
        cursor = conexion.cursor()
        cursor.execute("UPDATE clientes SET activo = 1 WHERE id = ?", (cliente_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente {cliente_id} reactivado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False