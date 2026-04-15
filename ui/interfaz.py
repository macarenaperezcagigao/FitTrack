# ui/interfaz.py
import customtkinter as ctk
from tkinter import messagebox
from config.settings import *
from db.clientes import obtener_clientes, obtener_cliente, eliminar_cliente, desactivar_cliente, reactivar_cliente
from db.progreso import obtener_progreso
from db.rutinas import obtener_rutinas
from db.sesiones import obtener_sesiones
from ui.ventanas import ventana_nuevo_cliente, ventana_editar_cliente

class App:
    """Interfaz principal de FitTrack - Moderno"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FitTrack - Gestor de Entrenamiento")
        self.root.geometry("1600x900")
        self.root.configure(fg_color=COLOR_FONDO)
        
        self.cliente_id = None
        self.cliente_nombre = None
        self.solo_activos = True
        
        self._crear_panel_lateral()
        self._crear_panel_principal()
        self._cargar_clientes()
    
    # ═══════════════════════════════════════════════════════════════
    # PANEL LATERAL
    # ═══════════════════════════════════════════════════════════════
    
    def _crear_panel_lateral(self):
        """Panel lateral con clientes"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_PANEL, width=300, corner_radius=0)
        frame.pack(side="left", fill="both", padx=0, pady=0)
        frame.pack_propagate(False)
        self.frame_lateral = frame
        
        # HEADER
        frame_header = ctk.CTkFrame(frame, fg_color="#c2185b", corner_radius=0, height=80)
        frame_header.pack(fill="x", padx=0, pady=0)
        frame_header.pack_propagate(False)
        
        ctk.CTkLabel(
            frame_header,
            text="💪 FITTRACK",
            font=("Arial", 18, "bold"),
            text_color=COLOR_TEXTO
        ).pack(pady=10)
        
        ctk.CTkLabel(
            frame_header,
            text="Entrenamiento",
            font=("Arial", 9),
            text_color=COLOR_TEXTO
        ).pack(pady=(0, 8))
        
        # BÚSQUEDA
        self.entrada_buscar = ctk.CTkEntry(
            frame,
            placeholder_text="🔍 Buscar...",
            width=270,
            text_color=COLOR_TEXTO,
            fg_color=COLOR_FONDO,
            border_color="#c2185b",
            border_width=1.5,
            font=("Arial", 10),
            corner_radius=8
        )
        self.entrada_buscar.pack(pady=10, padx=12)
        self.entrada_buscar.bind("<KeyRelease>", lambda e: self._filtrar_clientes())
        
        # FILTRO ACTIVOS/INACTIVOS
        frame_filtro = ctk.CTkFrame(frame, fg_color=COLOR_PANEL)
        frame_filtro.pack(fill="x", padx=12, pady=(8, 10))
        
        ctk.CTkLabel(frame_filtro, text="CLIENTES", font=("Arial", 10, "bold"), text_color=COLOR_TEXTO).pack(anchor="w", pady=(0, 5))
        
        self.switch_activos = ctk.CTkSwitch(
            frame_filtro,
            text="Mostrar inactivos",
            font=("Arial", 9),
            text_color=COLOR_TEXTO,
            command=self._cambiar_filtro
        )
        self.switch_activos.pack(anchor="w")
        
        # LISTA DE CLIENTES
        self.frame_clientes = ctk.CTkScrollableFrame(
            frame,
            fg_color=COLOR_PANEL,
            corner_radius=0
        )
        self.frame_clientes.pack(fill="both", expand=True, padx=8, pady=8)
        
        # BOTÓN NUEVO CLIENTE - VERDE
        self.btn_nuevo = ctk.CTkButton(
            frame,
            text="➕ NUEVO",
            fg_color="#4caf50",
            hover_color="#45a049",
            text_color=COLOR_TEXTO,
            width=270,
            font=("Arial", 11, "bold"),
            corner_radius=8,
            height=40,
            command=self._abrir_nuevo_cliente
        )
        self.btn_nuevo.pack(pady=10, padx=12, fill="x")
    
    def _cambiar_filtro(self):
        """Cambia el filtro de activos/inactivos"""
        self.solo_activos = not self.switch_activos.get()
        self._cargar_clientes()
    
    def _cargar_clientes(self):
        """Carga clientes en la lista"""
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()
        
        clientes = obtener_clientes(solo_activos=self.solo_activos)
        print(f"✅ Clientes cargados: {len(clientes)}")
        
        if not clientes:
            label = ctk.CTkLabel(
                self.frame_clientes,
                text="📭 Sin clientes",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 10)
            )
            label.pack(pady=30)
        else:
            for cliente in clientes:
                color_btn = "#9c27b0" if cliente['activo'] else "#666666"
                color_hover = "#7b1fa2" if cliente['activo'] else "#555555"
                
                btn = ctk.CTkButton(
                    self.frame_clientes,
                    text=f"👤 {cliente['nombre']}",
                    fg_color=color_btn,
                    hover_color=color_hover,
                    text_color=COLOR_TEXTO,
                    width=270,
                    font=("Arial", 10, "bold"),
                    corner_radius=8,
                    height=38,
                    command=lambda cid=cliente['id'], cn=cliente['nombre']: self._seleccionar_cliente(cid, cn)
                )
                btn.pack(pady=5, padx=0, fill="x")
    
    def _filtrar_clientes(self):
        """Filtra por búsqueda"""
        busqueda = self.entrada_buscar.get()
        
        for widget in self.frame_clientes.winfo_children():
            widget.destroy()
        
        conexion = __import__('sqlite3').connect("fittrack.db")
        cursor = conexion.cursor()
        
        if busqueda:
            cursor.execute(
                "SELECT * FROM clientes WHERE nombre LIKE ? AND activo = ?",
                (f"%{busqueda}%", 1 if self.solo_activos else 0)
            )
        else:
            cursor.execute("SELECT * FROM clientes WHERE activo = ?", (1 if self.solo_activos else 0,))
        
        clientes = cursor.fetchall()
        conexion.close()
        
        if not clientes:
            label = ctk.CTkLabel(
                self.frame_clientes,
                text="😕 Sin resultados",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 10)
            )
            label.pack(pady=30)
        else:
            for cliente in clientes:
                color_btn = "#9c27b0" if cliente[11] else "#666666"
                color_hover = "#7b1fa2" if cliente[11] else "#555555"
                
                btn = ctk.CTkButton(
                    self.frame_clientes,
                    text=f"👤 {cliente[1]}",
                    fg_color=color_btn,
                    hover_color=color_hover,
                    text_color=COLOR_TEXTO,
                    width=270,
                    font=("Arial", 10, "bold"),
                    corner_radius=8,
                    height=38,
                    command=lambda cid=cliente[0], cn=cliente[1]: self._seleccionar_cliente(cid, cn)
                )
                btn.pack(pady=5, padx=0, fill="x")
    
    # ═══════════════════════════════════════════════════════════════
    # PANEL PRINCIPAL
    # ═══════════════════════════════════════════════════════════════
    
    def _crear_panel_principal(self):
        """Panel derecho con recuadros azules"""
        frame = ctk.CTkFrame(self.root, fg_color=COLOR_FONDO, corner_radius=0)
        frame.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # TÍTULO
        self.titulo = ctk.CTkLabel(
            frame,
            text="👤 Selecciona un cliente",
            font=("Arial", 32, "bold"),
            text_color="#e91e63"
        )
        self.titulo.pack(pady=(0, 15), anchor="w")
        
        # INFORMACIÓN REDUCIDA
        frame_info_bg = ctk.CTkFrame(frame, fg_color="#1a1a2e", corner_radius=15)
        frame_info_bg.pack(fill="x", pady=(0, 15), padx=0)
        
        self.info = ctk.CTkLabel(
            frame_info_bg,
            text="",
            font=("Arial", 12),
            text_color=COLOR_TEXTO,
            justify="left"
        )
        self.info.pack(anchor="w", padx=20, pady=12)
        
        # BOTONES
        frame_botones = ctk.CTkFrame(frame, fg_color=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=(0, 15), anchor="w")
        
        self.btn_editar = ctk.CTkButton(
            frame_botones,
            text="✏️ EDITAR",
            fg_color="#9c27b0",
            hover_color="#7b1fa2",
            text_color=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            width=110,
            height=35,
            corner_radius=8,
            command=self._editar_cliente,
            state="disabled"
        )
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_desactivar = ctk.CTkButton(
            frame_botones,
            text="⏸️ PAUSAR",
            fg_color="#ff9800",
            hover_color="#f57300",
            text_color=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            width=110,
            height=35,
            corner_radius=8,
            command=self._desactivar_cliente,
            state="disabled"
        )
        self.btn_desactivar.pack(side="left", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(
            frame_botones,
            text="🗑️ ELIMINAR",
            fg_color="#f44336",
            hover_color="#d32f2f",
            text_color=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            width=110,
            height=35,
            corner_radius=8,
            command=self._eliminar_cliente,
            state="disabled"
        )
        self.btn_eliminar.pack(side="left", padx=5)
        
        # PESTAÑAS
        self.tabview = ctk.CTkTabview(
            frame,
            segmented_button_fg_color="#c2185b",
            text_color=COLOR_TEXTO,
            corner_radius=15,
            fg_color="#1a1a2e"
        )
        self.tabview.pack(fill="both", expand=True, pady=0)
        
        self.tab_clientes = self.tabview.add("👤 INFO")
        self.tab_progreso = self.tabview.add("📊 PROGRESO")
        self.tab_rutinas = self.tabview.add("💪 RUTINAS")
        self.tab_sesiones = self.tabview.add("📅 SESIONES")
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA: INFO
        # ════════════════════════════════════════════════════════════
        
        self.tab_clientes.configure(fg_color=COLOR_FONDO)
        
        frame_info_detail = ctk.CTkFrame(
            self.tab_clientes,
            fg_color="#1a1a2e",
            corner_radius=15
        )
        frame_info_detail.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            frame_info_detail,
            text="📋 Información Completa",
            font=("Arial", 16, "bold"),
            text_color="#e91e63"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        self.label_info_cliente = ctk.CTkLabel(
            frame_info_detail,
            text="Selecciona un cliente",
            font=("Arial", 12),
            text_color=COLOR_TEXTO,
            justify="left"
        )
        self.label_info_cliente.pack(anchor="w", padx=20, pady=(0, 15), fill="both", expand=True)
        
        # ═══════════════════════════���════════════════════════════════
        # PESTAÑA: PROGRESO
        # ════════════════════════════════════════════════════════════
        
        self.tab_progreso.configure(fg_color=COLOR_FONDO)
        
        frame_progreso_titulo = ctk.CTkFrame(self.tab_progreso, fg_color=COLOR_FONDO)
        frame_progreso_titulo.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            frame_progreso_titulo,
            text="📊 Registro de Medidas",
            font=("Arial", 14, "bold"),
            text_color="#e91e63"
        ).pack(side="left")
        
        self.btn_nuevo_progreso = ctk.CTkButton(
            frame_progreso_titulo,
            text="➕ Registrar",
            fg_color="#e91e63",
            hover_color="#c2185b",
            text_color=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            corner_radius=8,
            height=35,
            width=110,
            command=self._abrir_nuevo_progreso,
            state="disabled"
        )
        self.btn_nuevo_progreso.pack(side="right")
        
        self.frame_progreso_lista = ctk.CTkScrollableFrame(
            self.tab_progreso,
            fg_color=COLOR_FONDO,
            corner_radius=0
        )
        self.frame_progreso_lista.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA: RUTINAS
        # ════════════════════════════════════════════════════════════
        
        self.tab_rutinas.configure(fg_color=COLOR_FONDO)
        
        frame_rutinas_titulo = ctk.CTkFrame(self.tab_rutinas, fg_color=COLOR_FONDO)
        frame_rutinas_titulo.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            frame_rutinas_titulo,
            text="💪 Entrenamientos",
            font=("Arial", 14, "bold"),
            text_color="#e91e63"
        ).pack(side="left")
        
        self.btn_nueva_rutina = ctk.CTkButton(
            frame_rutinas_titulo,
            text="➕ Nueva",
            fg_color="#e91e63",
            hover_color="#c2185b",
            text_color=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            corner_radius=8,
            height=35,
            width=110,
            command=self._abrir_nueva_rutina,
            state="disabled"
        )
        self.btn_nueva_rutina.pack(side="right")
        
        self.frame_rutinas_lista = ctk.CTkScrollableFrame(
            self.tab_rutinas,
            fg_color=COLOR_FONDO,
            corner_radius=0
        )
        self.frame_rutinas_lista.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # ════════════════════════════════════════════════════════════
        # PESTAÑA: SESIONES
        # ════════════════════════════════════════════════════════════
        
        self.tab_sesiones.configure(fg_color=COLOR_FONDO)
        
        frame_sesiones_titulo = ctk.CTkFrame(self.tab_sesiones, fg_color=COLOR_FONDO)
        frame_sesiones_titulo.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            frame_sesiones_titulo,
            text="📅 Historial",
            font=("Arial", 14, "bold"),
            text_color="#e91e63"
        ).pack(side="left")
        
        self.btn_nueva_sesion = ctk.CTkButton(
            frame_sesiones_titulo,
            text="➕ Registrar",
            fg_color="#e91e63",
            hover_color="#c2185b",
            text_color=COLOR_TEXTO,
            font=("Arial", 10, "bold"),
            corner_radius=8,
            height=35,
            width=110,
            command=self._abrir_nueva_sesion,
            state="disabled"
        )
        self.btn_nueva_sesion.pack(side="right")
        
        self.frame_sesiones_lista = ctk.CTkScrollableFrame(
            self.tab_sesiones,
            fg_color=COLOR_FONDO,
            corner_radius=0
        )
        self.frame_sesiones_lista.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    
    # ═══════════════════════════════════════════════════════════════
    # SELECCIONAR CLIENTE
    # ═══════════════════════════════════════════════════════════════
    
    def _seleccionar_cliente(self, cliente_id, nombre):
        """Selecciona un cliente"""
        self.cliente_id = cliente_id
        self.cliente_nombre = nombre
        
        cliente = obtener_cliente(cliente_id)
        
        if cliente:
            self.titulo.configure(text=f"👤 {cliente['nombre']}")
            
            info = f"📝 {cliente['nombre']} | 🎂 {cliente['edad'] or 'N/A'} años | 📧 {cliente['email'] or 'N/A'}"
            self.info.configure(text=info)
            
            texto_btn = "⏸️ PAUSAR" if cliente['activo'] else "▶️ REACTIVAR"
            self.btn_desactivar.configure(text=texto_btn)
            
            self.btn_editar.configure(state="normal")
            self.btn_desactivar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
            self.btn_nuevo_progreso.configure(state="normal")
            self.btn_nueva_rutina.configure(state="normal")
            self.btn_nueva_sesion.configure(state="normal")
            
            self._cargar_info_cliente(cliente)
            self._cargar_progreso()
            self._cargar_rutinas()
            self._cargar_sesiones()
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA: INFO
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_info_cliente(self, cliente):
        """Muestra información completa"""
        info = (
            f"📝 Nombre: {cliente['nombre']}\n\n"
            f"🎂 Edad: {cliente['edad'] or 'N/A'} años\n"
            f"📧 Email: {cliente['email'] or 'N/A'}\n"
            f"📱 Teléfono: {cliente['telefono'] or 'N/A'}\n"
            f"👤 Género: {cliente['genero'] or 'N/A'}\n\n"
            f"⚖️ Peso: {cliente['peso'] or 'N/A'} kg\n"
            f"📏 Altura: {cliente['altura'] or 'N/A'} cm\n"
            f"💪 % Grasa: {cliente['grasa_corporal'] or 'N/A'}%\n\n"
            f"🎯 Objetivo: {cliente['objetivo'] or 'N/A'}\n"
            f"📋 Notas: {cliente['notas'] or 'N/A'}\n\n"
            f"🟢 Estado: {'ACTIVO' if cliente['activo'] else 'PAUSADO'}"
        )
        self.label_info_cliente.configure(text=info)
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA: PROGRESO
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_progreso(self):
        """Carga progreso"""
        for widget in self.frame_progreso_lista.winfo_children():
            widget.destroy()
        
        if not self.cliente_id:
            return
        
        progresos = obtener_progreso(self.cliente_id)
        
        if not progresos:
            label = ctk.CTkLabel(
                self.frame_progreso_lista,
                text="📭 Sin registros",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 13)
            )
            label.pack(pady=40)
        else:
            for progreso in progresos:
                frame_reg = ctk.CTkFrame(
                    self.frame_progreso_lista,
                    fg_color="#1a1a2e",
                    corner_radius=12
                )
                frame_reg.pack(fill="x", padx=0, pady=8)
                
                info_texto = (
                    f"📅 {progreso['fecha'][:10]} | "
                    f"⚖️ {progreso['peso']} kg | "
                    f"💪 {progreso['grasa_corporal']}% grasa"
                )
                ctk.CTkLabel(
                    frame_reg,
                    text=info_texto,
                    font=("Arial", 11, "bold"),
                    text_color="#e91e63"
                ).pack(anchor="w", padx=15, pady=(10, 5))
                
                medidas = f"Pecho: {progreso['pecho']}cm | Cintura: {progreso['cintura']}cm | Cadera: {progreso['cadera']}cm"
                ctk.CTkLabel(
                    frame_reg,
                    text=medidas,
                    font=("Arial", 10),
                    text_color=COLOR_TEXTO_SECUNDARIO
                ).pack(anchor="w", padx=15, pady=(0, 10))
    
    def _abrir_nuevo_progreso(self):
        """Abre ventana de progreso"""
        from ui.ventanas_progreso import ventana_nuevo_progreso
        ventana_nuevo_progreso(self.root, self.cliente_id, self._cargar_progreso)
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA: RUTINAS
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_rutinas(self):
        """Carga rutinas"""
        for widget in self.frame_rutinas_lista.winfo_children():
            widget.destroy()
        
        if not self.cliente_id:
            return
        
        rutinas = obtener_rutinas(self.cliente_id)
        
        if not rutinas:
            label = ctk.CTkLabel(
                self.frame_rutinas_lista,
                text="📭 Sin rutinas",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 13)
            )
            label.pack(pady=40)
        else:
            for rutina in rutinas:
                frame_rut = ctk.CTkFrame(
                    self.frame_rutinas_lista,
                    fg_color="#1a1a2e",
                    corner_radius=12
                )
                frame_rut.pack(fill="x", padx=0, pady=8)
                
                ctk.CTkLabel(
                    frame_rut,
                    text=f"💪 {rutina['nombre']}",
                    font=("Arial", 11, "bold"),
                    text_color="#e91e63"
                ).pack(anchor="w", padx=15, pady=(10, 5))
                
                ctk.CTkLabel(
                    frame_rut,
                    text=f"📅 {rutina['dias']}",
                    font=("Arial", 10),
                    text_color=COLOR_TEXTO_SECUNDARIO
                ).pack(anchor="w", padx=15, pady=(0, 10))
    
    def _abrir_nueva_rutina(self):
        """Abre ventana de rutina"""
        messagebox.showinfo("En desarrollo", "Funcionalidad próximamente")
    
    # ═══════════════════════════════════════════════════════════════
    # PESTAÑA: SESIONES
    # ═══════════════════════════════════════════════════════════════
    
    def _cargar_sesiones(self):
        """Carga sesiones"""
        for widget in self.frame_sesiones_lista.winfo_children():
            widget.destroy()
        
        if not self.cliente_id:
            return
        
        sesiones = obtener_sesiones(self.cliente_id)
        
        if not sesiones:
            label = ctk.CTkLabel(
                self.frame_sesiones_lista,
                text="📭 Sin sesiones",
                text_color=COLOR_TEXTO_SECUNDARIO,
                font=("Arial", 13)
            )
            label.pack(pady=40)
        else:
            for sesion in sesiones:
                frame_ses = ctk.CTkFrame(
                    self.frame_sesiones_lista,
                    fg_color="#1a1a2e",
                    corner_radius=12
                )
                frame_ses.pack(fill="x", padx=0, pady=8)
                
                info = f"📅 {sesion['fecha'][:10]} | 🏋️ {sesion['tipo']} | ⏱️ {sesion['duracion']} min"
                ctk.CTkLabel(
                    frame_ses,
                    text=info,
                    font=("Arial", 11, "bold"),
                    text_color="#e91e63"
                ).pack(anchor="w", padx=15, pady=(10, 5))
                
                estrellas = "⭐" * sesion['valoracion']
                ctk.CTkLabel(
                    frame_ses,
                    text=f"Valoración: {estrellas}",
                    font=("Arial", 10),
                    text_color=COLOR_TEXTO_SECUNDARIO
                ).pack(anchor="w", padx=15, pady=(0, 10))
    
    def _abrir_nueva_sesion(self):
        """Abre ventana de sesión"""
        messagebox.showinfo("En desarrollo", "Funcionalidad próximamente")
    
    # ═══════════════════════════════════════════════════════════════
    # BOTONES
    # ═══════════════════════════════════════════════════════════════
    
    def _abrir_nuevo_cliente(self):
        """Abre ventana de nuevo cliente"""
        ventana_nuevo_cliente(self.root, self._cargar_clientes)
    
    def _editar_cliente(self):
        """Edita cliente"""
        if not self.cliente_id:
            return
        ventana_editar_cliente(self.root, self.cliente_id, self._cargar_clientes)
    
    def _desactivar_cliente(self):
        """Desactiva o reactiva cliente"""
        if not self.cliente_id:
            return
        
        cliente = obtener_cliente(self.cliente_id)
        
        if cliente['activo']:
            if messagebox.askyesno("Pausar", f"¿Pausar a {self.cliente_nombre}?"):
                desactivar_cliente(self.cliente_id)
                messagebox.showinfo("Éxito", "⏸️ Cliente pausado")
                self._cargar_clientes()
                self._seleccionar_cliente(self.cliente_id, self.cliente_nombre)
        else:
            if messagebox.askyesno("Reactivar", f"¿Reactivar a {self.cliente_nombre}?"):
                reactivar_cliente(self.cliente_id)
                messagebox.showinfo("Éxito", "▶️ Cliente reactivado")
                self._cargar_clientes()
                self._seleccionar_cliente(self.cliente_id, self.cliente_nombre)
    
    def _eliminar_cliente(self):
        """Elimina cliente (RGPD)"""
        if not self.cliente_id:
            return
        
        if messagebox.askyesno("Eliminar", f"¿Eliminar PERMANENTEMENTE a {self.cliente_nombre}? (No se puede recuperar)"):
            eliminar_cliente(self.cliente_id)
            messagebox.showinfo("Éxito", "🗑️ Cliente eliminado")
            self._cargar_clientes()
            self.titulo.configure(text="👤 Selecciona un cliente")
            self.info.configure(text="")
            self.btn_editar.configure(state="disabled")
            self.btn_desactivar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
            self.btn_nuevo_progreso.configure(state="disabled")
            self.btn_nueva_rutina.configure(state="disabled")
            self.btn_nueva_sesion.configure(state="disabled")
            self.cliente_id = None