# app.py
import tkinter as tk
from tkinter import ttk
from state import AppState

FUENTE = ("Arial", 13)

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cronograma de Mantenimiento")
        self.root.minsize(800, 600)
        self._aplicar_estilos()
        self.state = AppState()
        self.frame_actual = None
        self.ir_a("periodo")

    def ir_a(self, pantalla: str, **kwargs):
        # Import local para evitar circular imports
        from screens.screen_periodo     import ScreenPeriodo
        from screens.screen_actividades import ScreenActividades
        from screens.screen_fechas      import ScreenFechas
        from screens.screen_resumen     import ScreenResumen
        from screens.screen_exito       import ScreenExito

        mapa = {
            "periodo":     ScreenPeriodo,
            "actividades": ScreenActividades,
            "fechas":      ScreenFechas,
            "resumen":     ScreenResumen,
            "exito":       ScreenExito,
        }
        if self.frame_actual:
            self.frame_actual.destroy()
        cls = mapa[pantalla]
        self.frame_actual = cls(self.root, self.state, self.ir_a, **kwargs)
        self.frame_actual.pack(fill="both", expand=True)

    def _aplicar_estilos(self):
        s = ttk.Style()
        s.configure(".", font=FUENTE)
        s.configure("TButton", padding=8)
        s.configure("Primary.TButton", font=("Arial", 13, "bold"))