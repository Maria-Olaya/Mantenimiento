import tkinter as tk
from tkinter import ttk, messagebox
from services.actividades import cargar_actividades, guardar_actividad, eliminar_actividad
from services.ortografia import corregir

class ScreenActividades(ttk.Frame):
    def __init__(self, master, state, navegar):
        super().__init__(master, padding=30)
        self.state   = state
        self.navegar = navegar
        self._checks = {}   # {nombre: BooleanVar}
        self._build()

    def _build(self):
        ttk.Label(self, text="Actividades del mes",
                  font=("Arial", 16, "bold")).pack(pady=(0, 16))

        # --- Lista con scroll ---
        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, highlightthickness=0)
        scroll = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        self._lista_frame = ttk.Frame(canvas)

        self._lista_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self._lista_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._render_lista()

        # --- Botones inferiores ---
        botones = ttk.Frame(self)
        botones.pack(fill="x", pady=16)

        ttk.Button(botones, text="← Atrás",
                   command=lambda: self.navegar("periodo")).pack(side="left", padx=6)
        ttk.Button(botones, text="+ Nueva actividad",
                   command=self._nueva_actividad).pack(side="left", padx=6)
        ttk.Button(botones, text="Continuar →",
                   style="Primary.TButton",
                   command=self._continuar).pack(side="right", padx=6)

    def _render_lista(self):
        for w in self._lista_frame.winfo_children():
            w.destroy()
        self._checks.clear()

        actividades = cargar_actividades()
        if not actividades:
            ttk.Label(self._lista_frame,
                      text="No tienes actividades aún. Agrega tu primera actividad.",
                      foreground="gray").pack(pady=20)
            return

        for nombre in actividades:
            fila = ttk.Frame(self._lista_frame)
            fila.pack(fill="x", pady=2)

            var = tk.BooleanVar(value=(nombre in self.state.actividades_seleccionadas))
            self._checks[nombre] = var
            ttk.Checkbutton(fila, text=nombre, variable=var,
                            style="TCheckbutton").pack(side="left", padx=4)
            ttk.Button(fila, text="✕", width=3,
                       command=lambda n=nombre: self._eliminar(n)).pack(side="right", padx=4)

    def _nueva_actividad(self):
        ventana = tk.Toplevel(self)
        ventana.title("Nueva actividad")
        ventana.grab_set()
        ventana.resizable(False, False)

        ttk.Label(ventana, text="Nombre de la actividad:", padding=10).pack()
        entry = ttk.Entry(ventana, width=36, font=("Arial", 13))
        entry.pack(padx=20, pady=4)
        entry.focus()

        def confirmar():
            texto = entry.get().strip()
            if not texto:
                messagebox.showwarning("Atención", "El nombre no puede estar vacío.",
                                       parent=ventana)
                return
            sugerido, hubo = corregir(texto)
            if hubo:
                self._sugerir_correccion(texto, sugerido, ventana)
            else:
                self._guardar_y_cerrar(texto, ventana)

        ttk.Button(ventana, text="Guardar", style="Primary.TButton",
                   command=confirmar).pack(pady=10)
        ventana.bind("<Return>", lambda e: confirmar())

    def _sugerir_correccion(self, original: str, sugerido: str, padre):
        v = tk.Toplevel(padre)
        v.title("Corrección ortográfica")
        v.grab_set()
        ttk.Label(v, text=f"¿Quisiste decir:\n\"{sugerido}\"?",
                  padding=16, font=("Arial", 13)).pack()
        btns = ttk.Frame(v)
        btns.pack(pady=8)
        ttk.Button(btns, text="Sí, usar esta",
                   command=lambda: [v.destroy(), padre.destroy(),
                                    self._guardar_y_cerrar(sugerido, None)]
                   ).pack(side="left", padx=6)
        ttk.Button(btns, text="No, dejar como está",
                   command=lambda: [v.destroy(), padre.destroy(),
                                    self._guardar_y_cerrar(original, None)]
                   ).pack(side="left", padx=6)
        ttk.Button(btns, text="Editar manualmente",
                   command=v.destroy).pack(side="left", padx=6)

    def _guardar_y_cerrar(self, nombre: str, ventana):
        try:
            guardar_actividad(nombre)
            self._render_lista()
            if ventana:
                ventana.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _eliminar(self, nombre: str):
        ok = messagebox.askyesno("Confirmar",
            f"¿Eliminar la actividad '{nombre}'?\nEsta acción no se puede deshacer.")
        if ok:
            eliminar_actividad(nombre)
            if nombre in self.state.actividades_seleccionadas:
                self.state.actividades_seleccionadas.remove(nombre)
            self._render_lista()

    def _continuar(self):
        seleccionadas = [n for n, v in self._checks.items() if v.get()]
        if not seleccionadas:
            messagebox.showwarning("Atención",
                "Selecciona al menos una actividad para continuar.")
            return
        self.state.actividades_seleccionadas = seleccionadas
        self.navegar("fechas")