import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from widgets.calendario import CalendarioMes
from services.evidencias import contar_evidencias

MESES_ES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

class ScreenFechas(ttk.Frame):
    def __init__(self, master, state, navegar):
        super().__init__(master, padding=20)
        self.state     = state
        self.navegar   = navegar
        self._calendarios = {}   # {nombre: CalendarioMes}
        self._build()

    def _build(self):
        mes_str = f"{MESES_ES[self.state.mes - 1]} {self.state.año}"
        ttk.Label(self, text=f"Fechas de actividades — {mes_str}",
                  font=("Arial", 16, "bold")).pack(pady=(0, 12))

        # --- Área scrollable ---
        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, highlightthickness=0)
        scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        inner  = ttk.Frame(canvas)

        inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Un calendario por actividad
        for nombre in self.state.actividades_seleccionadas:
            bloque = ttk.Frame(inner, padding=8)
            bloque.pack(fill="x", pady=6, padx=4)

            ttk.Label(bloque, text=nombre,
                      font=("Arial", 13, "bold")).pack(anchor="w", pady=(0, 4))

            dias_prev = self.state.dias_por_actividad.get(nombre, [])
            cal = CalendarioMes(bloque, self.state.año, self.state.mes, dias_prev)
            cal.pack(anchor="w")
            self._calendarios[nombre] = cal

        # --- Sección evidencias ---
        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", pady=10)

        ev_frame = ttk.Frame(self)
        ev_frame.pack(fill="x")

        ttk.Label(ev_frame, text="Evidencias del mes:",
                  font=("Arial", 13, "bold")).pack(side="left", padx=6)

        self._lbl_contador = ttk.Label(ev_frame, text=self._texto_contador())
        self._lbl_contador.pack(side="left", padx=6)

        ttk.Button(ev_frame, text="Agregar archivos",
                   command=self._agregar_archivos).pack(side="left", padx=6)

        # Lista de archivos cargados
        self._frame_archivos = ttk.Frame(self)
        self._frame_archivos.pack(fill="x", padx=6)
        self._render_archivos()

        # --- Navegación ---
        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=12)
        ttk.Button(nav, text="← Atrás",
                   command=lambda: self.navegar("actividades")).pack(side="left", padx=6)
        ttk.Button(nav, text="Revisar y guardar →",
                   style="Primary.TButton",
                   command=self._continuar).pack(side="right", padx=6)

    def _continuar(self):
        for nombre, cal in self._calendarios.items():
            if not cal.get_dias_marcados():
                messagebox.showwarning("Atención",
                    f"Marca al menos un día para la actividad '{nombre}'.")
                return
        # Escribir en state
        for nombre, cal in self._calendarios.items():
            self.state.dias_por_actividad[nombre] = cal.get_dias_marcados()
        self.navegar("resumen")

    def _agregar_archivos(self):
        rutas = filedialog.askopenfilenames(
            title="Selecciona archivos de evidencia")
        for r in rutas:
            if r not in self.state.archivos_evidencia:
                self.state.archivos_evidencia.append(r)
        self._render_archivos()
        self._lbl_contador.configure(text=self._texto_contador())

    def _render_archivos(self):
        for w in self._frame_archivos.winfo_children():
            w.destroy()
        for ruta in self.state.archivos_evidencia:
            fila = ttk.Frame(self._frame_archivos)
            fila.pack(fill="x", pady=1)
            ttk.Label(fila, text=Path(ruta).name,
                      foreground="#555").pack(side="left", padx=4)
            ttk.Button(fila, text="✕", width=3,
                       command=lambda r=ruta: self._quitar_archivo(r)).pack(side="right")

    def _quitar_archivo(self, ruta: str):
        self.state.archivos_evidencia.remove(ruta)
        self._render_archivos()
        self._lbl_contador.configure(text=self._texto_contador())

    def _texto_contador(self) -> str:
        ya = contar_evidencias(self.state.año, self.state.mes)
        nuevos = len(self.state.archivos_evidencia)
        return f"{ya} guardado(s) · {nuevos} nuevo(s) por cargar"