# ui/ventanas_progreso.py
import customtkinter as ctk
from tkinter import messagebox
from config.settings import *
from db.progreso import crear_progreso

def ventana_nuevo_progreso(parent, cliente_id, callback):
    """Abre ventana para registrar progreso"""
    ventana = ctk.CTkToplevel(parent)
    ventana.title("Registrar Progreso")
    ventana.geometry("550x700")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.transient(parent)
    ventana.grab_set()
    
    titulo = ctk.CTkLabel(ventana, text="📊 Registrar Medidas", font=("Arial", 18, "bold"), text_color=COLOR_TEXTO)
    titulo.pack(pady=15)
    
    # SCROLLABLE CON CAMPOS
    frame = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_PANEL, height=500)
    frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    campos = ["peso", "grasa", "pecho", "cintura", "cadera", "brazos", "piernas", "hombros", "notas"]
    etiquetas = ["⚖️ Peso (kg)", "💪 % Grasa", "📏 Pecho (cm)", "📏 Cintura (cm)", "📏 Cadera (cm)", 
                 "💪 Brazos (cm)", "🦵 Piernas (cm)", "📐 Hombros (cm)", "📝 Notas"]
    
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
        # Validar que al menos peso esté relleno
        peso_str = entradas["peso"].get().strip()
        if not peso_str:
            messagebox.showerror("Error", "❌ El peso es obligatorio")
            return
        
        # Validar peso es número
        try:
            peso = float(peso_str)
            if peso < 20 or peso > 250:
                messagebox.showerror("Error", "❌ El peso debe estar entre 20 y 250 kg")
                return
        except ValueError:
            messagebox.showerror("Error", "❌ El peso debe ser un número")
            return
        
        # Validar grasa si está rellena
        grasa_str = entradas["grasa"].get().strip()
        grasa = None
        if grasa_str:
            try:
                grasa = float(grasa_str)
                if grasa < 5 or grasa > 80:
                    messagebox.showerror("Error", "❌ El % de grasa debe estar entre 5 y 80")
                    return
            except ValueError:
                messagebox.showerror("Error", "❌ El % de grasa debe ser un número")
                return
        
        # Convertir medidas a float (opcional)
        def convertir_medida(valor_str):
            if not valor_str.strip():
                return None
            try:
                return float(valor_str)
            except ValueError:
                return None
        
        pecho = convertir_medida(entradas["pecho"].get())
        cintura = convertir_medida(entradas["cintura"].get())
        cadera = convertir_medida(entradas["cadera"].get())
        brazos = convertir_medida(entradas["brazos"].get())
        piernas = convertir_medida(entradas["piernas"].get())
        hombros = convertir_medida(entradas["hombros"].get())
        notas = entradas["notas"].get() or None
        
        # Guardar en BD
        exito = crear_progreso(
            cliente_id=cliente_id,
            peso=peso,
            grasa=grasa,
            pecho=pecho,
            cintura=cintura,
            cadera=cadera,
            brazos=brazos,
            piernas=piernas,
            hombros=hombros,
            notas=notas
        )
        
        if exito:
            messagebox.showinfo("Éxito", "✅ Progreso registrado")
            callback()  # Recarga la lista
            ventana.destroy()
        else:
            messagebox.showerror("Error", "❌ No se pudo registrar el progreso")
    
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