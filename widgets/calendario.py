import tkinter as tk
from tkinter import ttk
import calendar

DIAS_ES = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]

class CalendarioMes(ttk.Frame):
    def __init__(self, master, año, mes, dias_marcados=None):
        super().__init__(master, padding=8, relief="ridge")
        self.año  = año
        self.mes  = mes
        self._marcados = set(dias_marcados or [])
        self._botones  = {}
        self._build()

    def _build(self):
        for i, d in enumerate(DIAS_ES):
            ttk.Label(self, text=d, width=4,
                      anchor="center", font=("Arial", 10, "bold")).grid(
                row=0, column=i, padx=1, pady=2)

        primer_dia, total = calendar.monthrange(self.año, self.mes)
        fila, col = 1, primer_dia

        for dia in range(1, total + 1):
            btn = tk.Button(self, text=str(dia), width=3,
                            font=("Arial", 11),
                            relief="flat", cursor="hand2",
                            command=lambda d=dia: self._toggle(d))
            btn.grid(row=fila, column=col, padx=1, pady=1)
            self._botones[dia] = btn
            self._actualizar_color(dia)
            col += 1
            if col == 7:
                col, fila = 0, fila + 1

    def _toggle(self, dia: int):
        if dia in self._marcados:
            self._marcados.discard(dia)
        else:
            self._marcados.add(dia)
        self._actualizar_color(dia)

    def _actualizar_color(self, dia: int):
        btn = self._botones[dia]
        if dia in self._marcados:
            btn.configure(bg="#4CAF50", fg="white")
        else:
            btn.configure(bg="#F0F0F0", fg="#333333")

    def get_dias_marcados(self) -> list:
        return sorted(self._marcados)