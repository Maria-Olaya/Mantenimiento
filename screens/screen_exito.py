import os, sys
from tkinter import ttk
import tkinter as tk

class ScreenExito(ttk.Frame):
    def __init__(self, master, state, navegar):
        super().__init__(master, padding=40)
        self.state   = state
        self.navegar = navegar
        self._build()

    def _build(self):
        ttk.Label(self, text="✅ ¡Listo!",
                  font=("Arial", 22, "bold"),
                  foreground="#2E7D32").pack(pady=(20, 8))

        mes_str = _mes(self.state.mes)
        ttk.Label(self,
                  text=f"El informe de {mes_str} {self.state.año} fue guardado correctamente.",
                  font=("Arial", 13)).pack(pady=4)

        ttk.Label(self,
                  text=self.state.ruta_informe_guardado,
                  foreground="gray", font=("Arial", 11)).pack(pady=4)

        btns = ttk.Frame(self)
        btns.pack(pady=24)

        ttk.Button(btns, text="Abrir carpeta",
                   command=self._abrir_carpeta).pack(side="left", padx=10)
        ttk.Button(btns, text="Registrar otro mes",
                   style="Primary.TButton",
                   command=self._otro_mes).pack(side="left", padx=10)

    def _abrir_carpeta(self):
        import pathlib
        carpeta = str(pathlib.Path(self.state.ruta_informe_guardado).parent)
        if sys.platform == "win32":
            os.startfile(carpeta)
        elif sys.platform == "darwin":
            os.system(f'open "{carpeta}"')
        else:
            os.system(f'xdg-open "{carpeta}"')

    def _otro_mes(self):
        self.state.reset()
        self.navegar("periodo")

def _mes(n: int) -> str:
    return ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][n - 1]