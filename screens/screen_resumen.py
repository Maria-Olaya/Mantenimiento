from tkinter import ttk, messagebox
from services.excel import generar_excel
from services.evidencias import copiar_evidencias

MESES_ES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

class ScreenResumen(ttk.Frame):
    def __init__(self, master, state, navegar):
        super().__init__(master, padding=30)
        self.state   = state
        self.navegar = navegar
        self._build()

    def _build(self):
        mes_str = f"{MESES_ES[self.state.mes - 1]} {self.state.año}"
        ttk.Label(self, text=f"Resumen — {mes_str}",
                  font=("Arial", 16, "bold")).pack(pady=(0, 16))

        for nombre, dias in self.state.dias_por_actividad.items():
            dias_str = ", ".join(str(d) for d in sorted(dias))
            ttk.Label(self,
                      text=f"• {nombre}  →  días: {dias_str}",
                      font=("Arial", 12)).pack(anchor="w", pady=3)

        n_ev = len(self.state.archivos_evidencia)
        if n_ev:
            ttk.Label(self,
                      text=f"\n📎 {n_ev} archivo(s) de evidencia por guardar.",
                      foreground="#555").pack(anchor="w")

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=24)
        ttk.Button(nav, text="← Volver a editar",
                   command=lambda: self.navegar("fechas")).pack(side="left", padx=6)
        ttk.Button(nav, text="Guardar informe ✓",
                   style="Primary.TButton",
                   command=self._guardar).pack(side="right", padx=6)

    def _guardar(self):
        try:
            ruta = generar_excel(
                self.state.año,
                self.state.mes,
                self.state.dias_por_actividad
            )
            if self.state.archivos_evidencia:
                copiar_evidencias(
                    self.state.archivos_evidencia,
                    self.state.año,
                    self.state.mes
                )
            self.state.ruta_informe_guardado = str(ruta)
            self.navegar("exito")
        except PermissionError:
            messagebox.showerror("Archivo ocupado",
                "No se pudo guardar el informe.\n\n"
                "Si el archivo de este mes está abierto en Excel, "
                "ciérralo y vuelve a intentarlo.")
        except Exception as e:
            messagebox.showerror("Error al guardar",
                f"Ocurrió un error inesperado:\n{e}")