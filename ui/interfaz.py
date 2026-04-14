# ui/interfaz.py
import customtkinter as ctk
from tkinter import messagebox
from config.settings import *
from db.clientes import obtener_clientes, obtener_cliente, eliminar_cliente
from ui.ventanas import ventana_nuevo_cliente, ventana_editar_cliente

class App:
    """Interfaz principal de FitTrack"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FitTrack - Gestor de Clientes")
        self.root.geometry("1400x800")
        self.root.configure(fg_color=COLOR_FONDO)
        
        self.cliente_id = None
        self.cliente_nombre = None
        
        self._crear_panel_lateral()
        self._crear_panel_principal()
        self._cargar_clientes()
    
    def _crear_panel_lateral(self):
        """Panel lateral con clientes"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_PANEL, width=350)
        frame.pack(side="left", fill="both", padx=10, pady=10)
        frame.pack_propagate(False)
        self.frame_lateral = frame
        
        titulo = ctk.CTkLabel(frame, text="👥 CLIENTES", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
        titulo.pack(pady=10)
        
        self.entrada_buscar = ctk.CTkEntry(
            frame,
            placeholder_text="🔍 Buscar...",
            width=300,
            text_color=COLOR_TEXTO,
            fg_color=COLOR_FONDO,
            border_color=COLOR_SECUNDARIO,
            border_width=2,
            font=("Arial", 11)
        )
        self.entrada_buscar.pack(pady=8, padx=10)
        self.entrada_buscar.bind("<KeyRelease>", lambda e: self._filtrar_clientes())
        
        self.frame_clientes = ctk.CTkScrollableFrame(frame, fg_color=COLOR_PANEL)
        self.frame_clientes.pack(fill="both", expand=True, padx=5, pady=8)
        
        btn_nuevo = ctk.CTkButton(
            frame,
            text="➕ NUEVO CLIENTE",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            width=300,
            font=("Arial", 12, "bold"),
            command=self._abrir_nuevo_cliente
        )
        btn_nuevo.pack(pady=10, padx=10, fill="x")
    
    def _cargar_clientes(self):
        """Carga clientes en la lista"""
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()
        
        clientes = obtener_clientes()
        print(f"✅ Clientes: {len(clientes)}")
        
        if not clientes:
            label = ctk.CTkLabel(self.frame_clientes, text="📭 Sin clientes", text_color=COLOR_TEXTO, font=("Arial", 13))
            label.pack(pady=30)
        else:
            for cliente in clientes:
                btn = ctk.CTkButton(
                    self.frame_clientes,
                    text=cliente['nombre'],
                    fg_color=COLOR_PRIMARIO,
                    hover_color=COLOR_PRIMARIO_OSCURO,
                    text_color=COLOR_TEXTO,
                    width=310,
                    font=("Arial", 13),
                    command=lambda cid=cliente['id'], cn=cliente['nombre']: self._seleccionar_cliente(cid, cn)
                )
                btn.pack(pady=8, padx=5)
    
    def _filtrar_clientes(self):
        """Filtra por búsqueda"""
        busqueda = self.entrada_buscar.get()
        
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()
        
        clientes = obtener_clientes(busqueda)
        print(f"🔍 Búsqueda: {len(clientes)} resultados")
        
        if not clientes:
            label = ctk.CTkLabel(self.frame_clientes, text="😕 Sin resultados", text_color=COLOR_TEXTO, font=("Arial", 13))
            label.pack(pady=30)
        else:
            for cliente in clientes:
                btn = ctk.CTkButton(
                    self.frame_clientes,
                    text=cliente['nombre'],
                    fg_color=COLOR_PRIMARIO,
                    hover_color=COLOR_PRIMARIO_OSCURO,
                    text_color=COLOR_TEXTO,
                    width=310,
                    font=("Arial", 13),
                    command=lambda cid=cliente['id'], cn=cliente['nombre']: self._seleccionar_cliente(cid, cn)
                )
                btn.pack(pady=8, padx=5)
    
    def _crear_panel_principal(self):
        """Panel derecho con detalles"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_PANEL)
        frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.titulo = ctk.CTkLabel(frame, text="Selecciona un cliente", font=("Arial", 24, "bold"), text_color=COLOR_TEXTO)
        self.titulo.pack(pady=20)
        
        self.info = ctk.CTkLabel(frame, text="", font=("Arial", 13), text_color=COLOR_TEXTO, justify="left")
        self.info.pack(pady=15, padx=30)
        
        frame_botones = ctk.CTkFrame(frame, fg_color=COLOR_PANEL)
        frame_botones.pack(fill="x", padx=30, pady=10)
        
        self.btn_editar = ctk.CTkButton(
            frame_botones,
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
            frame_botones,
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
        
        frame_pestanas = ctk.CTkFrame(frame, fg_color=COLOR_PANEL)
        frame_pestanas.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkButton(frame_pestanas, text="📅 SESIONES", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_SECUNDARIO_OSCURO, text_color=COLOR_TEXTO, font=("Arial", 11, "bold"), width=140, state="disabled").pack(side="left", padx=5)
        ctk.CTkButton(frame_pestanas, text="💪 RUTINAS", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_SECUNDARIO_OSCURO, text_color=COLOR_TEXTO, font=("Arial", 11, "bold"), width=140, state="disabled").pack(side="left", padx=5)
        ctk.CTkButton(frame_pestanas, text="📊 PROGRESO", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_SECUNDARIO_OSCURO, text_color=COLOR_TEXTO, font=("Arial", 11, "bold"), width=140, state="disabled").pack(side="left", padx=5)
        ctk.CTkButton(frame_pestanas, text="📝 NOTAS", fg_color=COLOR_SECUNDARIO, hover_color=COLOR_SECUNDARIO_OSCURO, text_color=COLOR_TEXTO, font=("Arial", 11, "bold"), width=140, state="disabled").pack(side="left", padx=5)
        
        self.contenido = ctk.CTkLabel(frame, text="Selecciona un cliente", font=("Arial", 14), text_color=COLOR_TEXTO_SECUNDARIO)
        self.contenido.pack(pady=50)
    
    def _seleccionar_cliente(self, cliente_id, nombre):
        """Selecciona cliente"""
        self.cliente_id = cliente_id
        self.cliente_nombre = nombre
        
        cliente = obtener_cliente(cliente_id)
        
        if cliente:
            self.titulo.configure(text=f"👤 {cliente['nombre']}")
            info = f"Edad: {cliente['edad']}\nEmail: {cliente['email']}\nTeléfono: {cliente['telefono']}\nGénero: {cliente['genero']}\nPeso: {cliente['peso']} kg"
            self.info.configure(text=info)
            
            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
            self.contenido.configure(text=f"✅ {nombre}\n\nSelecciona una pestaña")
    
    def _abrir_nuevo_cliente(self):
        ventana_nuevo_cliente(self.root, self._cargar_clientes)
    
    def _editar_cliente(self):
        if not self.cliente_id:
            return
        ventana_editar_cliente(self.root, self.cliente_id, self._cargar_clientes)
    
    def _eliminar_cliente(self):
        if not self.cliente_id:
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {self.cliente_nombre}?"):
            eliminar_cliente(self.cliente_id)
            messagebox.showinfo("Éxito", "✅ Cliente eliminado")
            self._cargar_clientes()
            self.titulo.configure(text="Selecciona un cliente")
            self.info.configure(text="")
            self.btn_editar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
            self.cliente_id = None