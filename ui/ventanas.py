# ui/ventanas.py
import re
import customtkinter as ctk
from tkinter import messagebox
from config.settings import *
from db.clientes import crear_cliente, obtener_cliente, actualizar_cliente

# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════

def validar_email(email):
    """Comprueba que el email tenga formato correcto"""
    if not email:
        return True  # Si está vacío, es opcional
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Comprueba que tenga exactamente 9 dígitos"""
    if not telefono:
        return True  # Si está vacío, es opcional
    return telefono.isdigit() and len(telefono) == 9

def validar_edad(edad_str):
    """Valida que la edad sea un número entre 0 y 120"""
    if not edad_str:
        return True, None  # Si está vacío, es opcional
    try:
        edad = int(edad_str)
        if edad < 0 or edad > 120:
            return False, "La edad debe estar entre 0 y 120 años"
        return True, edad
    except ValueError:
        return False, "La edad debe ser un número"

def validar_peso(peso_str):
    """Valida que el peso sea un número entre 20 y 250 kg"""
    if not peso_str:
        return True, None  # Si está vacío, es opcional
    try:
        peso = float(peso_str)
        if peso < 20 or peso > 250:
            return False, "El peso debe estar entre 20 y 250 kg"
        return True, peso
    except ValueError:
        return False, "El peso debe ser un número"

def validar_altura(altura_str):
    """Valida que la altura sea un número entre 100 y 250 cm"""
    if not altura_str:
        return True, None  # Si está vacío, es opcional
    try:
        altura = float(altura_str)
        if altura < 100 or altura > 250:
            return False, "La altura debe estar entre 100 y 250 cm"
        return True, altura
    except ValueError:
        return False, "La altura debe ser un número"

def validar_grasa(grasa_str):
    """Valida que el % de grasa sea un número entre 5 y 80"""
    if not grasa_str:
        return True, None  # Si está vacío, es opcional
    try:
        grasa = float(grasa_str)
        if grasa < 5 or grasa > 80:
            return False, "El % de grasa debe estar entre 5 y 80"
        return True, grasa
    except ValueError:
        return False, "El % de grasa debe ser un número"

# ═══════════════════════════════════════════════════════════════
# VENTANA: CREAR NUEVO CLIENTE
# ═══════════════════════════════════════════════════════════════

def ventana_nuevo_cliente(parent, callback):
    """Abre ventana para crear nuevo cliente"""
    ventana = ctk.CTkToplevel(parent)
    ventana.title("Nuevo Cliente")
    ventana.geometry("550x700")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.transient(parent)
    ventana.grab_set()
    
    titulo = ctk.CTkLabel(ventana, text="📝 Nuevo Cliente", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=15)
    
    # SCROLLABLE CON CAMPOS
    frame = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_PANEL, height=500)
    frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    campos = ["nombre", "edad", "email", "telefono", "genero", "peso", "altura", "grasa", "objetivo", "notas"]
    etiquetas = ["📝 Nombre*", "🎂 Edad", "📧 Email", "📱 Teléfono", "👤 Género", "⚖️ Peso (kg)", "📏 Altura (cm)", "💪 % Grasa", "🎯 Objetivo", "📋 Notas"]
    
    entradas = {}
    
    for campo, etiqueta in zip(campos, etiquetas):
        lbl = ctk.CTkLabel(frame, text=etiqueta, text_color=COLOR_TEXTO, font=("Arial", 11, "bold"))
        lbl.pack(anchor="w", padx=5, pady=(8, 2))
        
        entrada = ctk.CTkEntry(
            frame,
            placeholder_text=etiqueta,
            width=480,
            text_color=COLOR_TEXTO,
            fg_color=COLOR_FONDO,
            border_color=COLOR_SECUNDARIO,
            border_width=1,
            font=("Arial", 11)
        )
        entrada.pack(padx=5, pady=2)
        entradas[campo] = entrada
    
    # BOTONES - FIJO EN ABAJO
    frame_botones = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO, height=60)
    frame_botones.pack(fill="x", padx=15, pady=10)
    frame_botones.pack_propagate(False)
    
    def guardar():
        # VALIDAR NOMBRE (OBLIGATORIO)
        nombre = entradas["nombre"].get().strip()
        if not nombre:
            messagebox.showerror("Error", "❌ El nombre es obligatorio")
            return
        
        # VALIDAR EMAIL (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDO)
        email = entradas["email"].get().strip()
        if email and not validar_email(email):
            messagebox.showerror("Error", "❌ Email inválido\nFormato correcto: algo@algo.com")
            return
        
        # VALIDAR TELÉFONO (OPCIONAL, PERO SI SE RELLENA DEBE TENER 9 DÍGITOS)
        telefono = entradas["telefono"].get().strip()
        if telefono and not validar_telefono(telefono):
            messagebox.showerror("Error", "❌ Teléfono inválido\nDebe tener exactamente 9 dígitos")
            return
        
        # VALIDAR EDAD (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        edad_valida, edad = validar_edad(entradas["edad"].get().strip())
        if not edad_valida:
            messagebox.showerror("Error", f"❌ {edad}")
            return
        
        # VALIDAR PESO (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        peso_valida, peso = validar_peso(entradas["peso"].get().strip())
        if not peso_valida:
            messagebox.showerror("Error", f"❌ {peso}")
            return
        
        # VALIDAR ALTURA (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        altura_valida, altura = validar_altura(entradas["altura"].get().strip())
        if not altura_valida:
            messagebox.showerror("Error", f"❌ {altura}")
            return
        
        # VALIDAR GRASA (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        grasa_valida, grasa = validar_grasa(entradas["grasa"].get().strip())
        if not grasa_valida:
            messagebox.showerror("Error", f"❌ {grasa}")
            return
        
        # SI TODO ES VÁLIDO, CREAR CLIENTE
        exito = crear_cliente(
            nombre=nombre,
            edad=edad,
            email=email or None,
            telefono=telefono or None,
            genero=entradas["genero"].get() or None,
            peso=peso or 0,
            altura=altura or 0,
            grasa=grasa or 0,
            objetivo=entradas["objetivo"].get() or None,
            notas=entradas["notas"].get() or None
        )
        
        if exito:
            messagebox.showinfo("Éxito", f"✅ Cliente '{nombre}' creado correctamente")
            callback()
            ventana.destroy()
        else:
            messagebox.showerror("Error", "❌ Este cliente ya existe (nombre duplicado)")
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="✅ GUARDAR",
        fg_color=COLOR_PRIMARIO,
        hover_color=COLOR_PRIMARIO_OSCURO,
        text_color=COLOR_TEXTO,
        font=("Arial", 12, "bold"),
        width=220,
        command=guardar
    )
    btn_guardar.pack(side="left", padx=5, pady=10)
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ CANCELAR",
        fg_color="#666666",
        hover_color="#555555",
        text_color=COLOR_TEXTO,
        font=("Arial", 12, "bold"),
        width=220,
        command=ventana.destroy
    )
    btn_cancelar.pack(side="left", padx=5, pady=10)

# ═══════════════════════════════════════════════════════════════
# VENTANA: EDITAR CLIENTE
# ═══════════════════════════════════════════════════════════════

def ventana_editar_cliente(parent, cliente_id, callback):
    """Abre ventana para editar cliente"""
    cliente = obtener_cliente(cliente_id)
    
    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado")
        return
    
    ventana = ctk.CTkToplevel(parent)
    ventana.title("Editar Cliente")
    ventana.geometry("550x700")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.transient(parent)
    ventana.grab_set()
    
    titulo = ctk.CTkLabel(ventana, text=f"✏️ Editar: {cliente['nombre']}", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=15)
    
    # SCROLLABLE CON CAMPOS
    frame = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_PANEL, height=500)
    frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    campos = ["nombre", "edad", "email", "telefono", "genero", "peso", "altura", "grasa", "objetivo", "notas"]
    etiquetas = ["📝 Nombre*", "🎂 Edad", "📧 Email", "📱 Teléfono", "👤 Género", "⚖️ Peso (kg)", "📏 Altura (cm)", "💪 % Grasa", "🎯 Objetivo", "📋 Notas"]
    
    entradas = {}
    
    for campo, etiqueta in zip(campos, etiquetas):
        lbl = ctk.CTkLabel(frame, text=etiqueta, text_color=COLOR_TEXTO, font=("Arial", 11, "bold"))
        lbl.pack(anchor="w", padx=5, pady=(8, 2))
        
        entrada = ctk.CTkEntry(
            frame,
            placeholder_text=etiqueta,
            width=480,
            text_color=COLOR_TEXTO,
            fg_color=COLOR_FONDO,
            border_color=COLOR_SECUNDARIO,
            border_width=1,
            font=("Arial", 11)
        )
        
        # Insertar el valor actual del cliente
        valor = cliente.get(campo)
        if valor is not None:
            entrada.insert(0, str(valor))
        
        entrada.pack(padx=5, pady=2)
        entradas[campo] = entrada
    
    # BOTONES - FIJO EN ABAJO
    frame_botones = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO, height=60)
    frame_botones.pack(fill="x", padx=15, pady=10)
    frame_botones.pack_propagate(False)
    
    def guardar():
        # VALIDAR NOMBRE (OBLIGATORIO)
        nombre = entradas["nombre"].get().strip()
        if not nombre:
            messagebox.showerror("Error", "❌ El nombre es obligatorio")
            return
        
        # VALIDAR EMAIL (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDO)
        email = entradas["email"].get().strip()
        if email and not validar_email(email):
            messagebox.showerror("Error", "❌ Email inválido\nFormato correcto: algo@algo.com")
            return
        
        # VALIDAR TELÉFONO (OPCIONAL, PERO SI SE RELLENA DEBE TENER 9 DÍGITOS)
        telefono = entradas["telefono"].get().strip()
        if telefono and not validar_telefono(telefono):
            messagebox.showerror("Error", "❌ Teléfono inválido\nDebe tener exactamente 9 dígitos")
            return
        
        # VALIDAR EDAD (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        edad_valida, edad = validar_edad(entradas["edad"].get().strip())
        if not edad_valida:
            messagebox.showerror("Error", f"❌ {edad}")
            return
        
        # VALIDAR PESO (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        peso_valida, peso = validar_peso(entradas["peso"].get().strip())
        if not peso_valida:
            messagebox.showerror("Error", f"❌ {peso}")
            return
        
        # VALIDAR ALTURA (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        altura_valida, altura = validar_altura(entradas["altura"].get().strip())
        if not altura_valida:
            messagebox.showerror("Error", f"❌ {altura}")
            return
        
        # VALIDAR GRASA (OPCIONAL, PERO SI SE RELLENA DEBE SER VÁLIDA)
        grasa_valida, grasa = validar_grasa(entradas["grasa"].get().strip())
        if not grasa_valida:
            messagebox.showerror("Error", f"❌ {grasa}")
            return
        
        # SI TODO ES VÁLIDO, ACTUALIZAR CLIENTE
        exito = actualizar_cliente(
            cliente_id,
            nombre=nombre,
            edad=edad,
            email=email or None,
            telefono=telefono or None,
            genero=entradas["genero"].get() or None,
            peso=peso or 0,
            altura=altura or 0,
            grasa=grasa or 0,
            objetivo=entradas["objetivo"].get() or None,
            notas=entradas["notas"].get() or None
        )
        
        if exito:
            messagebox.showinfo("Éxito", "✅ Cliente actualizado correctamente")
            callback()
            ventana.destroy()
        else:
            messagebox.showerror("Error", "❌ No se pudo actualizar el cliente")
    
    btn_guardar = ctk.CTkButton(
        frame_botones,
        text="✅ GUARDAR",
        fg_color=COLOR_PRIMARIO,
        hover_color=COLOR_PRIMARIO_OSCURO,
        text_color=COLOR_TEXTO,
        font=("Arial", 12, "bold"),
        width=220,
        command=guardar
    )
    btn_guardar.pack(side="left", padx=5, pady=10)
    
    btn_cancelar = ctk.CTkButton(
        frame_botones,
        text="❌ CANCELAR",
        fg_color="#666666",
        hover_color="#555555",
        text_color=COLOR_TEXTO,
        font=("Arial", 12, "bold"),
        width=220,
        command=ventana.destroy
    )
    btn_cancelar.pack(side="left", padx=5, pady=10)