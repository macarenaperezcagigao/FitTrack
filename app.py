# app.py
import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# COLORES
COLOR_PRIMARIO = "#2E7D32"
COLOR_PRIMARIO_OSCURO = "#1B4620"
COLOR_SECUNDARIO = "#1565C0"
COLOR_SECUNDARIO_OSCURO = "#0D47A1"
COLOR_FONDO = "#1E1E1E"
COLOR_PANEL = "#2D2D2D"
COLOR_TEXTO = "#FFFFFF"
COLOR_TEXTO_SECUNDARIO = "#CCCCCC"
COLOR_ERROR = "#D32F2F"

RUTA_DB = "fittrack.db"

# ═══════════════════════════════════════════════════════════════════
# BASE DE DATOS
# ═══════════════════════════════════════════════════════════════════

def crear_tablas():
    """Crea tablas en la BD"""
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
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rutinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            dias_semana TEXT,
            descripcion TEXT,
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
            descanso_segundos INTEGER,
            notas TEXT,
            FOREIGN KEY (rutina_id) REFERENCES rutinas(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duracion_minutos INTEGER,
            tipo_sesion TEXT,
            valoracion INTEGER,
            notas TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    
    conexion.commit()
    conexion.close()
    print("✅ Base de datos iniciada")

# ─────────────────────────────────────────────────────────────────
# CLIENTES
# ─────────────────────────────────────────────────────────────────

def obtener_clientes(busqueda=""):
    """Obtiene clientes de la BD"""
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
    """Obtiene un cliente por ID"""
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conexion.close()
    return dict(cliente) if cliente else None

def crear_cliente(nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas):
    """Crea un cliente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, edad, email, telefono, genero, peso, altura, grasa_corporal, objetivo, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente '{nombre}' creado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def actualizar_cliente(cliente_id, nombre, edad, email, telefono, genero, peso, altura, grasa, objetivo, notas):
    """Actualiza un cliente"""
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
        print(f"✅ Cliente actualizado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def eliminar_cliente(cliente_id):
    """Elimina un cliente"""
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexion.commit()
        conexion.close()
        print(f"✅ Cliente eliminado")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════
# INTERFAZ
# ═══════════════════════════════════════════════════════════════════

class FitTrackApp:
    """Aplicación FitTrack"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FitTrack - Gestor de Clientes")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        self.root.configure(fg_color=COLOR_FONDO)
        
        self.cliente_id = None
        self.cliente_nombre = None
        
        # Inicializar BD
        crear_tablas()
        
        # Crear interfaz
        self._panel_lateral()
        self._panel_principal()
        
        # Cargar clientes
        self._cargar_clientes()
        print("✅ Aplicación lista")
    
    # ═════════════════════════════════════════════════════════════
    # PANEL LATERAL (Izquierda)
    # ═════════════════════════════════════════════════════════════
    
    def _panel_lateral(self):
        """Crea panel lateral con lista de clientes"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_PANEL, width=350)
        frame.pack(side="left", fill="both", padx=10, pady=10)
        frame.pack_propagate(False)
        self.frame_lateral = frame
        
        # Título
        titulo = ctk.CTkLabel(frame, text="👥 CLIENTES", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
        titulo.pack(pady=15)
        
        # Buscador
        self.entrada_buscar = ctk.CTkEntry(
            frame,
            placeholder_text="🔍 Buscar cliente...",
            width=320,
            text_color=COLOR_TEXTO,
            fg_color=COLOR_FONDO,
            border_color=COLOR_SECUNDARIO,
            border_width=2,
            font=("Arial", 12)
        )
        self.entrada_buscar.pack(pady=10, padx=10)
        self.entrada_buscar.bind("<KeyRelease>", lambda e: self._filtrar_clientes())
        
        # Frame scrollable para clientes
        self.frame_clientes = ctk.CTkScrollableFrame(frame, fg_color=COLOR_PANEL, width=330)
        self.frame_clientes.pack(fill="both", expand=True, padx=5, pady=10)
        self.frame_clientes.pack_propagate(False)
        
        # Botón nuevo cliente
        btn_nuevo = ctk.CTkButton(
            frame,
            text="➕ NUEVO CLIENTE",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            width=320,
            font=("Arial", 13, "bold"),
            command=self._nuevo_cliente
        )
        btn_nuevo.pack(pady=10, padx=10)
    
    def _cargar_clientes(self):
        """Carga clientes en la lista"""
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()
        
        clientes = obtener_clientes()
        print(f"📋 Clientes en BD: {len(clientes)}")
        
        if not clientes:
            label = ctk.CTkLabel(
                self.frame_clientes,
                text="📭 Sin clientes\nCrea uno nuevo",
                text_color=COLOR_TEXTO,
                font=("Arial", 13)
            )
            label.pack(pady=30)
        else:
            for cliente in clientes:
                nombre = cliente['nombre']
                cliente_id = cliente['id']
                btn = ctk.CTkButton(
                    self.frame_clientes,
                    text=nombre,
                    fg_color=COLOR_PRIMARIO,
                    hover_color=COLOR_PRIMARIO_OSCURO,
                    text_color=COLOR_TEXTO,
                    width=310,
                    font=("Arial", 13),
                    command=lambda cid=cliente_id, cn=nombre: self._seleccionar_cliente(cid, cn)
                )
                btn.pack(pady=8, padx=5)
    
    def _filtrar_clientes(self):
        """Filtra clientes por búsqueda"""
        busqueda = self.entrada_buscar.get()
        
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()
        
        clientes = obtener_clientes(busqueda)
        print(f"🔍 Búsqueda: '{busqueda}' - Resultados: {len(clientes)}")
        
        if not clientes:
            label = ctk.CTkLabel(
                self.frame_clientes,
                text="😕 Sin resultados",
                text_color=COLOR_TEXTO,
                font=("Arial", 13)
            )
            label.pack(pady=30)
        else:
            for cliente in clientes:
                nombre = cliente['nombre']
                cliente_id = cliente['id']
                btn = ctk.CTkButton(
                    self.frame_clientes,
                    text=nombre,
                    fg_color=COLOR_PRIMARIO,
                    hover_color=COLOR_PRIMARIO_OSCURO,
                    text_color=COLOR_TEXTO,
                    width=310,
                    font=("Arial", 13),
                    command=lambda cid=cliente_id, cn=nombre: self._seleccionar_cliente(cid, cn)
                )
                btn.pack(pady=8, padx=5)
    
    # ══════════════════════════════════════��══════════════════════
    # PANEL PRINCIPAL (Derecha)
    # ═════════════════════════════════════════════════════════════
    
    def _panel_principal(self):
        """Crea panel principal con detalle del cliente"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_PANEL)
        frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Título
        self.titulo = ctk.CTkLabel(
            frame,
            text="Selecciona un cliente",
            font=("Arial", 24, "bold"),
            text_color=COLOR_TEXTO
        )
        self.titulo.pack(pady=20)
        
        # Información del cliente
        self.info = ctk.CTkLabel(
            frame,
            text="",
            font=("Arial", 13),
            text_color=COLOR_TEXTO,
            justify="left"
        )
        self.info.pack(pady=15, padx=30)
        
        # BOTONES EDITAR Y ELIMINAR
        frame_botones_accion = ctk.CTkFrame(frame, fg_color=COLOR_PANEL)
        frame_botones_accion.pack(fill="x", padx=30, pady=10)
        
        self.btn_editar = ctk.CTkButton(
            frame_botones_accion,
            text="✏️ EDITAR",
            fg_color=COLOR_SECUNDARIO,
            hover_color=COLOR_SECUNDARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 12, "bold"),
            width=150,
            command=self._editar_cliente,
            state="disabled"
        )
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(
            frame_botones_accion,
            text="🗑️ ELIMINAR",
            fg_color=COLOR_ERROR,
            hover_color="#B71C1C",
            text_color=COLOR_TEXTO,
            font=("Arial", 12, "bold"),
            width=150,
            command=self._eliminar_cliente,
            state="disabled"
        )
        self.btn_eliminar.pack(side="left", padx=5)
        
        # PESTAÑAS
        frame_pestanas = ctk.CTkFrame(frame, fg_color=COLOR_PANEL)
        frame_pestanas.pack(fill="x", padx=30, pady=10)
        
        self.btn_sesiones = ctk.CTkButton(
            frame_pestanas,
            text="📅 SESIONES",
            fg_color=COLOR_SECUNDARIO,
            hover_color=COLOR_SECUNDARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            width=140,
            state="disabled"
        )
        self.btn_sesiones.pack(side="left", padx=5)
        
        self.btn_rutinas = ctk.CTkButton(
            frame_pestanas,
            text="💪 RUTINAS",
            fg_color=COLOR_SECUNDARIO,
            hover_color=COLOR_SECUNDARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            width=140,
            state="disabled"
        )
        self.btn_rutinas.pack(side="left", padx=5)
        
        self.btn_progreso = ctk.CTkButton(
            frame_pestanas,
            text="📊 PROGRESO",
            fg_color=COLOR_SECUNDARIO,
            hover_color=COLOR_SECUNDARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            width=140,
            state="disabled"
        )
        self.btn_progreso.pack(side="left", padx=5)
        
        self.btn_notas = ctk.CTkButton(
            frame_pestanas,
            text="📝 NOTAS",
            fg_color=COLOR_SECUNDARIO,
            hover_color=COLOR_SECUNDARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            width=140,
            state="disabled"
        )
        self.btn_notas.pack(side="left", padx=5)
        
        # CONTENIDO
        self.contenido = ctk.CTkLabel(
            frame,
            text="Selecciona un cliente para ver su información",
            font=("Arial", 14),
            text_color=COLOR_TEXTO_SECUNDARIO
        )
        self.contenido.pack(pady=50)
    
    def _seleccionar_cliente(self, cliente_id, nombre):
        """Selecciona un cliente y muestra su info"""
        self.cliente_id = cliente_id
        self.cliente_nombre = nombre
        
        cliente = obtener_cliente(cliente_id)
        
        if cliente:
            # Actualizar título
            self.titulo.configure(text=f"👤 {cliente['nombre']}")
            
            # Actualizar información
            info_texto = f"""
Edad: {cliente['edad']} años
Email: {cliente['email']}
Teléfono: {cliente['telefono']}
Género: {cliente['genero']}
Peso: {cliente['peso']} kg
Altura: {cliente['altura']} cm
% Grasa: {cliente['grasa_corporal']}%
Objetivo: {cliente['objetivo']}
Notas: {cliente['notas']}
            """
            self.info.configure(text=info_texto)
            
            # Habilitar botones
            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
            self.btn_sesiones.configure(state="normal")
            self.btn_rutinas.configure(state="normal")
            self.btn_progreso.configure(state="normal")
            self.btn_notas.configure(state="normal")
            
            # Actualizar contenido
            self.contenido.configure(text=f"✅ {nombre}\n\nSelecciona una pestaña para ver detalles")
    
    # ═════════════════════════════════════════════════════════════
    # FORMULARIOS
    # ═════════════════════════════════════════════════════════════
    
    def _nuevo_cliente(self):
        """Abre formulario para crear nuevo cliente"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Nuevo Cliente")
        ventana.geometry("500x650")
        ventana.configure(fg_color=COLOR_FONDO)
        ventana.transient(self.root)
        ventana.grab_set()
        
        titulo = ctk.CTkLabel(ventana, text="📝 Nuevo Cliente", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
        titulo.pack(pady=20)
        
        frame = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_PANEL)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        campos = ["nombre", "edad", "email", "telefono", "genero", "peso", "altura", "grasa", "objetivo", "notas"]
        etiquetas = ["📝 Nombre*", "🎂 Edad", "📧 Email", "📱 Teléfono", "👤 Género", "⚖️ Peso (kg)", "📏 Altura (cm)", "💪 % Grasa", "🎯 Objetivo", "📋 Notas"]
        
        entradas = {}
        
        for campo, etiqueta in zip(campos, etiquetas):
            lbl = ctk.CTkLabel(frame, text=etiqueta, text_color=COLOR_TEXTO, font=("Arial", 12, "bold"))
            lbl.pack(anchor="w", padx=5, pady=(10, 3))
            
            entrada = ctk.CTkEntry(
                frame,
                placeholder_text=etiqueta,
                width=450,
                text_color=COLOR_TEXTO,
                fg_color=COLOR_FONDO,
                border_color=COLOR_SECUNDARIO,
                border_width=2,
                font=("Arial", 11)
            )
            entrada.pack(padx=5, pady=3)
            entradas[campo] = entrada
        
        frame_botones = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
        frame_botones.pack(fill="x", padx=20, pady=15)
        
        def guardar():
            nombre = entradas["nombre"].get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            exito = crear_cliente(
                nombre=nombre,
                edad=entradas["edad"].get() or None,
                email=entradas["email"].get() or None,
                telefono=entradas["telefono"].get() or None,
                genero=entradas["genero"].get() or None,
                peso=float(entradas["peso"].get() or 0),
                altura=float(entradas["altura"].get() or 0),
                grasa=float(entradas["grasa"].get() or 0),
                objetivo=entradas["objetivo"].get() or None,
                notas=entradas["notas"].get() or None
            )
            
            if exito:
                messagebox.showinfo("Éxito", f"✅ Cliente '{nombre}' creado correctamente")
                self._cargar_clientes()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "❌ No se pudo crear el cliente")
        
        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="✅ GUARDAR",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 12, "bold"),
            width=200,
            command=guardar
        )
        btn_guardar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="❌ CANCELAR",
            fg_color="#666666",
            hover_color="#555555",
            text_color=COLOR_TEXTO,
            font=("Arial", 12, "bold"),
            width=200,
            command=ventana.destroy
        )
        btn_cancelar.pack(side="left", padx=5)
    
    def _editar_cliente(self):
        """Abre formulario para editar cliente"""
        if not self.cliente_id:
            messagebox.showwarning("Aviso", "Selecciona un cliente")
            return
        
        cliente = obtener_cliente(self.cliente_id)
        
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Editar Cliente")
        ventana.geometry("500x650")
        ventana.configure(fg_color=COLOR_FONDO)
        ventana.transient(self.root)
        ventana.grab_set()
        
        titulo = ctk.CTkLabel(ventana, text=f"✏️ Editar: {cliente['nombre']}", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
        titulo.pack(pady=20)
        
        frame = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_PANEL)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        campos = ["nombre", "edad", "email", "telefono", "genero", "peso", "altura", "grasa", "objetivo", "notas"]
        etiquetas = ["📝 Nombre*", "🎂 Edad", "📧 Email", "📱 Teléfono", "👤 Género", "⚖️ Peso (kg)", "📏 Altura (cm)", "💪 % Grasa", "🎯 Objetivo", "📋 Notas"]
        
        entradas = {}
        
        for campo, etiqueta in zip(campos, etiquetas):
            lbl = ctk.CTkLabel(frame, text=etiqueta, text_color=COLOR_TEXTO, font=("Arial", 12, "bold"))
            lbl.pack(anchor="w", padx=5, pady=(10, 3))
            
            entrada = ctk.CTkEntry(
                frame,
                placeholder_text=etiqueta,
                width=450,
                text_color=COLOR_TEXTO,
                fg_color=COLOR_FONDO,
                border_color=COLOR_SECUNDARIO,
                border_width=2,
                font=("Arial", 11)
            )
            entrada.insert(0, str(cliente[campo]) if cliente[campo] else "")
            entrada.pack(padx=5, pady=3)
            entradas[campo] = entrada
        
        frame_botones = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
        frame_botones.pack(fill="x", padx=20, pady=15)
        
        def guardar():
            actualizar_cliente(
                self.cliente_id,
                nombre=entradas["nombre"].get(),
                edad=entradas["edad"].get() or None,
                email=entradas["email"].get() or None,
                telefono=entradas["telefono"].get() or None,
                genero=entradas["genero"].get() or None,
                peso=float(entradas["peso"].get() or 0),
                altura=float(entradas["altura"].get() or 0),
                grasa=float(entradas["grasa"].get() or 0),
                objetivo=entradas["objetivo"].get() or None,
                notas=entradas["notas"].get() or None
            )
            
            messagebox.showinfo("Éxito", "✅ Cliente actualizado")
            self._cargar_clientes()
            self._seleccionar_cliente(self.cliente_id, entradas["nombre"].get())
            ventana.destroy()
        
        btn_guardar = ctk.CTkButton(
            frame_botones,
            text="✅ GUARDAR",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 12, "bold"),
            width=200,
            command=guardar
        )
        btn_guardar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="❌ CANCELAR",
            fg_color="#666666",
            hover_color="#555555",
            text_color=COLOR_TEXTO,
            font=("Arial", 12, "bold"),
            width=200,
            command=ventana.destroy
        )
        btn_cancelar.pack(side="left", padx=5)
    
    def _eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        if not self.cliente_id:
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar a {self.cliente_nombre}?\n\n⚠️ Se eliminarán también sus sesiones y rutinas."
        )
        
        if respuesta:
            eliminar_cliente(self.cliente_id)
            messagebox.showinfo("Éxito", f"✅ {self.cliente_nombre} eliminado")
            self._cargar_clientes()
            
            # Limpiar panel
            self.titulo.configure(text="Selecciona un cliente")
            self.info.configure(text="")
            self.contenido.configure(text="Selecciona un cliente para ver su información")
            self.btn_editar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
            self.btn_sesiones.configure(state="disabled")
            self.btn_rutinas.configure(state="disabled")
            self.btn_progreso.configure(state="disabled")
            self.btn_notas.configure(state="disabled")
            
            self.cliente_id = None
            self.cliente_nombre = None