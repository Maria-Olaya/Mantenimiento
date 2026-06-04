import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from services.config import cargar_config, guardar_config, carpeta_fuente
from services.excel import informe_existe, leer_informe

MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
         "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

class ScreenPeriodo(ttk.Frame):
    def __init__(self, master, state, navegar):
        super().__init__(master, padding=40)
        self.state   = state
        self.navegar = navegar
        self._build()

    def _build(self):
        ttk.Label(self, text="Cronograma de Mantenimiento",
                  font=("Arial", 18, "bold")).pack(pady=(0, 30))

        # --- Selector mes/año ---
        fila = ttk.Frame(self)
        fila.pack()

        ttk.Label(fila, text="Mes:").grid(row=0, column=0, padx=8)
        self.cb_mes = ttk.Combobox(fila, values=MESES, state="readonly", width=14)
        self.cb_mes.grid(row=0, column=1, padx=8)

        ttk.Label(fila, text="Año:").grid(row=0, column=2, padx=8)
        año_actual = date.today().year
        años = [str(y) for y in range(año_actual, año_actual + 10)]
        self.cb_año = ttk.Combobox(fila, values=años, state="readonly", width=8)
        self.cb_año.grid(row=0, column=3, padx=8)

        # Precargar si ya había selección
        if self.state.mes:
            self.cb_mes.current(self.state.mes - 1)
        if self.state.año:
            self.cb_año.set(str(self.state.año))

        ttk.Button(self, text="Continuar →",
                   style="Primary.TButton",
                   command=self._continuar).pack(pady=30)

        # --- Carpeta fuente ---
        self._var_carpeta = tk.StringVar(value=str(carpeta_fuente()))
        pie = ttk.Frame(self)
        pie.pack(side="bottom", fill="x", pady=10)
        ttk.Label(pie, textvariable=self._var_carpeta,
                  foreground="gray").pack(side="left", padx=8)
        ttk.Button(pie, text="Cambiar carpeta",
                   command=self._cambiar_carpeta).pack(side="left")

    def _continuar(self):
        if not self.cb_mes.get() or not self.cb_año.get():
            messagebox.showwarning("Atención",
                "Por favor selecciona el mes y el año antes de continuar.")
            return

        self.state.mes = MESES.index(self.cb_mes.get()) + 1
        self.state.año = int(self.cb_año.get())

        if informe_existe(self.state.año, self.state.mes):
            self._preguntar_modo()
        else:
            self.state.modo = "nuevo"
            self.navegar("actividades")

    def _preguntar_modo(self):
        mes_str = MESES[self.state.mes - 1]
        ventana = tk.Toplevel(self)
        ventana.title("Informe existente")
        ventana.grab_set()
        ttk.Label(ventana, padding=20,
                  text=f"Ya existe un informe para {mes_str} {self.state.año}.\n"
                       "¿Qué deseas hacer?").pack()
        btns = ttk.Frame(ventana)
        btns.pack(pady=10)
        ttk.Button(btns, text="Editar existente",
                   command=lambda: self._elegir("editar", ventana)).pack(side="left", padx=8)
        ttk.Button(btns, text="Crear nuevo",
                   command=lambda: self._elegir("nuevo", ventana)).pack(side="left", padx=8)

    def _elegir(self, modo: str, ventana):
        ventana.destroy()
        self.state.modo = modo
        if modo == "editar":
            self.state.dias_por_actividad = leer_informe(self.state.año, self.state.mes)
            self.state.actividades_seleccionadas = list(self.state.dias_por_actividad.keys())
        self.navegar("actividades")

    def _cambiar_carpeta(self):
        from tkinter.filedialog import askdirectory
        ruta = askdirectory(title="Selecciona la carpeta donde guardar los informes")
        if ruta:
            guardar_config({"carpeta_fuente": ruta})
            self._var_carpeta.set(ruta)