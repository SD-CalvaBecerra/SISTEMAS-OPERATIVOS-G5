import tkinter as tk
from tkinter import ttk
from direcciones.swapping import Swapping


class PanelMarcos:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.resultado = None
        self.paso_actual = 0
        self.labels_marcos = []

        self.marco_display = tk.Frame(contenedor)
        self.marco_display.pack(fill="both", expand=True, padx=10, pady=5)

        self.lbl_pagina = tk.Label(
            self.marco_display, text="", font=("Courier", 14), width=10
        )
        self.lbl_pagina.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_estado = tk.Label(
            self.marco_display, text="", font=("Courier", 12), width=28
        )
        self.lbl_estado.grid(row=1, column=0, columnspan=4, pady=5)

        self.lbl_swap = tk.Label(
            self.marco_display, text="", font=("Courier", 10)
        )
        self.lbl_swap.grid(row=2, column=0, columnspan=8, sticky="w", padx=5, pady=2)

        self.btn_ant = ttk.Button(self.marco_display, text="< Anterior", command=self.anterior)
        self.btn_ant.grid(row=3, column=0, padx=5, pady=5)

        self.btn_sig = ttk.Button(self.marco_display, text="Siguiente >", command=self.siguiente)
        self.btn_sig.grid(row=3, column=1, padx=5, pady=5)

        self.btn_play = ttk.Button(self.marco_display, text="▶ Reproducir", command=self.reproducir)
        self.btn_play.grid(row=3, column=2, padx=5, pady=5)

        self.auto_id = None

    def _crear_marcos(self, n):
        for lbl in self.labels_marcos:
            lbl.destroy()
        self.labels_marcos.clear()
        for i in range(n):
            lbl = tk.Label(
                self.marco_display,
                text=f"M{i}",
                font=("Courier", 12),
                width=6,
                height=2,
                relief="groove",
                bg="lightgray",
            )
            lbl.grid(row=0, column=i + 2, padx=5, pady=5)
            self.labels_marcos.append(lbl)

    def mostrar(self, resultado):
        if self.auto_id is not None:
            self.contenedor.after_cancel(self.auto_id)
            self.auto_id = None
            self.btn_play.configure(text="▶ Reproducir")
        self.resultado = resultado
        self.paso_actual = 0
        n = resultado["num_marcos"]
        self._crear_marcos(n)
        self._dibujar_paso()

    def _dibujar_paso(self):
        if not self.resultado or self.paso_actual >= len(self.resultado["pasos"]):
            return

        paso = self.resultado["pasos"][self.paso_actual]
        n = self.resultado["num_marcos"]
        afectado = paso["marco_afectado"]

        for idx, lbl in enumerate(self.labels_marcos):
            if idx < n:
                valor = paso["marcos"][idx]
                txt = str(valor) if valor is not None else "-"
                if idx == afectado and paso["reemplazada"] is not None:
                    color = "#ffcccc"
                elif idx == afectado and paso["fallo"]:
                    color = "#fff3cd"
                elif valor is not None:
                    color = "white"
                else:
                    color = "lightgray"
                lbl.configure(text=txt, bg=color)
            else:
                lbl.configure(text="-", bg="lightgray")

        self.lbl_pagina.configure(text=f"Página: {paso['pagina']}")

        estado_texto = "OK" if not paso["fallo"] else "FALLO"
        if paso["reemplazada"] is not None:
            estado_texto += f" (sale {paso['reemplazada']})"

        self.lbl_estado.configure(
            text=estado_texto,
            fg="red" if paso["fallo"] else "green",
        )

        swap = Swapping()
        for p in self.resultado["pasos"][:self.paso_actual + 1]:
            if p["reemplazada"] is not None:
                swap.guardar_pagina(p["reemplazada"], f"pág_{p['reemplazada']}")
            if p["fallo"]:
                swap.eliminar_pagina(p["pagina"])

        disco = sorted(swap.disco.keys())
        if paso["reemplazada"] is not None:
            swap_txt = f"Swap: sale pág. {paso['reemplazada']} -> disco | entra pág. {paso['pagina']} -> M{afectado}"
        elif paso["fallo"]:
            swap_txt = f"Carga: entra pág. {paso['pagina']} -> M{afectado}"
        else:
            swap_txt = "Sin swap (acierto en RAM)"
        self.lbl_swap.configure(text=f"{swap_txt} | En disco: {disco}")

    def anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self._dibujar_paso()

    def siguiente(self):
        if self.paso_actual < len(self.resultado["pasos"]) - 1:
            self.paso_actual += 1
            self._dibujar_paso()

    def reproducir(self):
        if self.auto_id is not None:
            self.contenedor.after_cancel(self.auto_id)
            self.auto_id = None
            self.btn_play.configure(text="▶ Reproducir")
            return

        self.auto_id = self.contenedor.after(300, self._avanzar_auto)
        self.btn_play.configure(text="⏸ Pausar")

    def _avanzar_auto(self):
        if self.paso_actual < len(self.resultado["pasos"]) - 1:
            self.paso_actual += 1
            self._dibujar_paso()
            self.auto_id = self.contenedor.after(300, self._avanzar_auto)
        else:
            self.auto_id = None
            self.btn_play.configure(text="▶ Reproducir")
