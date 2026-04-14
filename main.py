# main.py
import customtkinter as ctk
from db.database import crear_tablas
from ui.interfaz import App

if __name__ == "__main__":
    print("🚀 Iniciando FitTrack...")
    
    crear_tablas()
    
    app = ctk.CTk()
    fittrack = App(app)
    
    app.mainloop()
    print("👋 FitTrack cerrado")