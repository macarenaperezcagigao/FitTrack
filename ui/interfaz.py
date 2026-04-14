# ui/interfaz.py
import customtkinter as ctk
from tkinter import messagebox
from config.settings import *
from db.clientes import obtener_clientes, obtener_cliente, eliminar_cliente
from db.progreso import obtener_progreso
from db.rutinas import obtener_rutinas
from db.sesiones import obtener_sesiones
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
    
    # ═══════════════════════════════════════════════════════════════
    # PANEL LATERAL - Lista de clientes
    # ═══════════════════════════════════════════════════════════════
    
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
        print(f"✅ Clientes cargados: {len(clientes)}")
        
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
    
    # ═══════════════════════════════════════════════════════════════
    # PANEL PRINCIPAL - Detalles y pestañas
    # ═══════════════════════════════════════════════════════════════
    
    def _crear_panel_principal(self):
        """Panel derecho con detalles y pestañas"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_PANEL)
        frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # TÍTULO DEL CLIENTE
        self.titulo = ctk.CTkLabel(
            frame, 
            text="Selecciona un cliente", 
            font=("Arial", 24, "bold"), 
            text_color=COLOR_TEXTO
        )
        self.titulo.pack(pady=20)
        
        # BOTONES EDITAR / ELIMINAR
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
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑAS
        # ════════════════════════════════════════════════════════════
        
        self.tabview = ctk.CTkTabview(
            frame, 
            segmented_button_fg_color=COLOR_SECUNDARIO,
            text_color=COLOR_TEXTO
        )
        self.tabview.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Crear 4 pestañas
        self.tab_clientes = self.tabview.add("👤 CLIENTES")
        self.tab_progreso = self.tabview.add("📊 PROGRESO")
        self.tab_rutinas = self.tabview.add("💪 RUTINAS")
        self.tab_sesiones = self.tabview.add("📅 SESIONES")
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA 1: CLIENTES (información completa)
        # ════════════════════════════════════════════════════════════
        
        frame_info_cliente = ctk.CTkFrame(self.tab_clientes, fg_color=COLOR_PANEL, corner_radius=8)
        frame_info_cliente.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame_info_cliente,
            text="📋 Información del Cliente",
            font=("Arial", 16, "bold"),
            text_color=COLOR_TEXTO
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        self.label_info_cliente = ctk.CTkLabel(
            frame_info_cliente,
            text="Selecciona un cliente",
            font=("Arial", 13),
            text_color=COLOR_TEXTO,
            justify="left"
        )
        self.label_info_cliente.pack(anchor="w", padx=20, pady=10, fill="both", expand=True)
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA 2: PROGRESO (medidas)
        # ════════════════════════════════════════════════════════════
        
        frame_progreso_titulo = ctk.CTkFrame(self.tab_progreso, fg_color=COLOR_PANEL)
        frame_progreso_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_progreso_titulo,
            text="📊 Registro de Progreso",
            font=("Arial", 16, "bold"),
            text_color=COLOR_TEXTO
        ).pack(side="left", padx=10)
        
        self.btn_nuevo_progreso = ctk.CTkButton(
            frame_progreso_titulo,
            text="➕ Registrar Medidas",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            command=self._abrir_nuevo_progreso,
            state="disabled"
        )
        self.btn_nuevo_progreso.pack(side="right", padx=10)
        
        # Área scrollable para historial de progreso
        self.frame_progreso_lista = ctk.CTkScrollableFrame(
            self.tab_progreso,
            fg_color=COLOR_FONDO
        )
        self.frame_progreso_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA 3: RUTINAS (entrenamientos)
        # ════════════════════════════════════════════════════════════
        
        frame_rutinas_titulo = ctk.CTkFrame(self.tab_rutinas, fg_color=COLOR_PANEL)
        frame_rutinas_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_rutinas_titulo,
            text="💪 Rutinas de Entrenamiento",
            font=("Arial", 16, "bold"),
            text_color=COLOR_TEXTO
        ).pack(side="left", padx=10)
        
        self.btn_nueva_rutina = ctk.CTkButton(
            frame_rutinas_titulo,
            text="➕ Nueva Rutina",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            command=self._abrir_nueva_rutina,
            state="disabled"
        )
        self.btn_nueva_rutina.pack(side="right", padx=10)
        
        # Área scrollable para rutinas
        self.frame_rutinas_lista = ctk.CTkScrollableFrame(
            self.tab_rutinas,
            fg_color=COLOR_FONDO
        )
        self.frame_rutinas_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA 4: SESIONES (entrenamientos realizados)
        # ════════════════════════════════════════════════════════════
        
        frame_sesiones_titulo = ctk.CTkFrame(self.tab_sesiones, fg_color=COLOR_PANEL)
        frame_sesiones_titulo.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_sesiones_titulo,
            text="📅 Historial de Sesiones",
            font=("Arial", 16, "bold"),
            text_color=COLOR_TEXTO
        ).pack(side="left", padx=10)
        
        self.btn_nueva_sesion = ctk.CTkButton(
            frame_sesiones_titulo,
            text="➕ Registrar Sesión",
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_OSCURO,
            text_color=COLOR_TEXTO,
            font=("Arial", 11, "bold"),
            command=self._abrir_nueva_sesion,
            state="disabled"
        )
        self.btn_nueva_sesion.pack(side="right", padx=10)
        
        # Área scrollable para sesiones
        self.frame_sesiones_lista = ctk.CTkScrollableFrame(
            self.tab_sesiones,
            fg_color=COLOR_FONDO
        )
        self.frame_sesiones_lista.pack(fill="both", expand=True, padx=20, pady=10)
    
    # ═══════════════════════════════════════════════════════════════
    # SELECCIONAR CLIENTE
    # ═══════════════════════════════════════════════════════════════
    
    def _seleccionar_cliente(self, cliente_id, nombre):
        """Selecciona un cliente y carga sus datos"""
        self.cliente_id = cliente_id
        self.cliente_nombre = nombre
        
        cliente = obtener_cliente(cliente_id)
        
        if cliente:
            # Actualizar título
            self.titulo.configure(text=f"👤 {cliente['nombre']}")
            
            # Habilitar botones
            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
            self.btn_nuevo_progreso.configure(state="normal")
            self.btn_nueva_rutina.configure(state="normal")
            self.btn_nueva_sesion.configure(state="normal")
            
            # Cargar datos en las pestañas
            self._cargar_info_cliente(cliente)
            self._cargar_progreso()
            self._cargar_rutinas()
            self._cargar_sesiones()
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA CLIENTES
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_info_cliente(self, cliente):
        """Muestra información completa del cliente en pestaña CLIENTES"""
        info_cliente = (
            f"📝 Nombre: {cliente['nombre']}\n"
            f"🎂 Edad: {cliente['edad'] or 'N/A'} años\n"
            f"📧 Email: {cliente['email'] or 'N/A'}\n"
            f"📱 Teléfono: {cliente['telefono'] or 'N/A'}\n"
            f"👤 Género: {cliente['genero'] or 'N/A'}\n"
            f"⚖️ Peso: {cliente['peso'] or 'N/A'} kg\n"
            f"📏 Altura: {cliente['altura'] or 'N/A'} cm\n"
            f"💪 % Grasa: {cliente['grasa_corporal'] or 'N/A'}%\n"
            f"🎯 Objetivo: {cliente['objetivo'] or 'N/A'}\n"
            f"📋 Notas: {cliente['notas'] or 'N/A'}"
        )
        self.label_info_cliente.configure(text=info_cliente)
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA PROGRESO
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_progreso(self):
        """Carga el historial de progreso del cliente"""
        for widget in self.frame_progreso_lista.winfo_children():
            widget.destroy()
        
        if not self.cliente_id:
            return
        
        progresos = obtener_progreso(self.cliente_id)
        
        if not progresos:
            label = ctk.CTkLabel(
                self.frame_progreso_lista,
                text="📭 Sin registros de progreso",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 13)
            )
            label.pack(pady=30)
        else:
            for progreso in progresos:
                frame_reg = ctk.CTkFrame(self.frame_progreso_lista, fg_color=COLOR_PANEL, corner_radius=8)
                frame_reg.pack(fill="x", padx=10, pady=8)
                
                info_texto = (
                    f"📅 {progreso['fecha'][:10]} | "
                    f"⚖️ {progreso['peso']} kg | "
                    f"💪 {progreso['grasa_corporal']}% grasa"
                )
                ctk.CTkLabel(
                    frame_reg,
                    text=info_texto,
                    font=("Arial", 11, "bold"),
                    text_color=COLOR_TEXTO
                ).pack(anchor="w", padx=15, pady=8)
                
                medidas_texto = (
                    f"Pecho: {progreso['pecho']}cm | "
                    f"Cintura: {progreso['cintura']}cm | "
                    f"Cadera: {progreso['cadera']}cm"
                )
                ctk.CTkLabel(
                    frame_reg,
                    text=medidas_texto,
                    font=("Arial", 10),
                    text_color=COLOR_TEXTO_SECUNDARIO
                ).pack(anchor="w", padx=15, pady=4)
    
    def _abrir_nuevo_progreso(self):
        """Abre ventana para registrar progreso"""
        from ui.ventanas_progreso import ventana_nuevo_progreso
        ventana_nuevo_progreso(self.root, self.cliente_id, self._cargar_progreso)
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA RUTINAS
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_rutinas(self):
        """Carga las rutinas del cliente"""
        for widget in self.frame_rutinas_lista.winfo_children():
            widget.destroy()
        
        if not self.cliente_id:
            return
        
        rutinas = obtener_rutinas(self.cliente_id)
        
        if not rutinas:
            label = ctk.CTkLabel(
                self.frame_rutinas_lista,
                text="📭 Sin rutinas creadas",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 13)
            )
            label.pack(pady=30)
        else:
            for rutina in rutinas:
                frame_rut = ctk.CTkFrame(self.frame_rutinas_lista, fg_color=COLOR_PANEL, corner_radius=8)
                frame_rut.pack(fill="x", padx=10, pady=8)
                
                ctk.CTkLabel(
                    frame_rut,
                    text=f"💪 {rutina['nombre']}",
                    font=("Arial", 12, "bold"),
                    text_color=COLOR_TEXTO
                ).pack(anchor="w", padx=15, pady=8)
                
                ctk.CTkLabel(
                    frame_rut,
                    text=f"📅 {rutina['dias']}",
                    font=("Arial", 10),
                    text_color=COLOR_TEXTO_SECUNDARIO
                ).pack(anchor="w", padx=15, pady=4)
    
    def _abrir_nueva_rutina(self):
        """Abre ventana para crear rutina"""
        messagebox.showinfo("Próximamente", "Funcionalidad en desarrollo")
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA SESIONES
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_sesiones(self):
        """Carga el historial de sesiones del cliente"""
        for widget in self.frame_sesiones_lista.winfo_children():
            widget.destroy()
        
        if not self.cliente_id:
            return
        
        sesiones = obtener_sesiones(self.cliente_id)
        
        if not sesiones:
            label = ctk.CTkLabel(
                self.frame_sesiones_lista,
                text="📭 Sin sesiones registradas",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 13)
            )
            label.pack(pady=30)
        else:
            for sesion in sesiones:
                frame_ses = ctk.CTkFrame(self.frame_sesiones_lista, fg_color=COLOR_PANEL, corner_radius=8)
                frame_ses.pack(fill="x", padx=10, pady=8)
                
                info_texto = (
                    f"📅 {sesion['fecha'][:10]} | "
                    f"🏋️ {sesion['tipo']} | "
                    f"⏱️ {sesion['duracion']} min"
                )
                ctk.CTkLabel(
                    frame_ses,
                    text=info_texto,
                    font=("Arial", 11, "bold"),
                    text_color=COLOR_TEXTO
                ).pack(anchor="w", padx=15, pady=8)
                
                estrellas = "⭐" * sesion['valoracion']
                ctk.CTkLabel(
                    frame_ses,
                    text=f"Valoración: {estrellas}",
                    font=("Arial", 10),
                    text_color=COLOR_TEXTO_SECUNDARIO
                ).pack(anchor="w", padx=15, pady=4)
    
    def _abrir_nueva_sesion(self):
        """Abre ventana para registrar sesión"""
        messagebox.showinfo("Próximamente", "Funcionalidad en desarrollo")
    
    # ═══════════════════════════════════════════════════════════════
    # CLIENTE - EDITAR Y ELIMINAR
    # ═══════════════════════════════════════════════════════════════
    
    def _abrir_nuevo_cliente(self):
        """Abre ventana para crear nuevo cliente"""
        ventana_nuevo_cliente(self.root, self._cargar_clientes)
    
    def _editar_cliente(self):
        """Abre ventana para editar cliente"""
        if not self.cliente_id:
            return
        ventana_editar_cliente(self.root, self.cliente_id, self._cargar_clientes)
    
    def _eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        if not self.cliente_id:
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {self.cliente_nombre}?"):
            eliminar_cliente(self.cliente_id)
            messagebox.showinfo("Éxito", "✅ Cliente eliminado")
            self._cargar_clientes()
            self.titulo.configure(text="Selecciona un cliente")
            self.btn_editar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
            self.btn_nuevo_progreso.configure(state="disabled")
            self.btn_nueva_rutina.configure(state="disabled")
            self.btn_nueva_sesion.configure(state="disabled")
            self.cliente_id = None