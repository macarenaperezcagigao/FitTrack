# db/clientes.py
# Funciones de clientes

import sqlite3
from config.settings import RUTA_DB

def obtener_clientes(busqueda=""):
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    if busqueda:
        cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ? ORDER BY nombre", (f"%{busqueda}%",))
    else:
        cursor.execute("SELECT * FROM clientes ORDER BY nombre")
    
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

def obtener_cliente(cliente_id):
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conexion.close()
    return dict(cliente) if cliente else None

def crear_cliente(nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al crear: {e}")
        return False

def actualizar_cliente(cliente_id, nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET nombre=?, edad=?, email=?, telefono=?, genero=?, peso=?, altura=?, grasa_corporal=?, objetivo=?, notas=?
            WHERE id = ?
        """, (nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas, cliente_id))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False

def eliminar_cliente(cliente_id):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al eliminar: {e}")
        return False