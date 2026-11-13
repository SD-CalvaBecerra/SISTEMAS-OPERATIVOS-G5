import tkinter as tk
from tkinter import ttk

class PanelMarcos:
    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.pasos = []
        self.indice = 0
        self.reproduciendo = False

        self.frame = ttk.LabelFrame(contenedor, text="Marcos de Memoria", padding=10)
        self.frame.pack(fill="both", expand=True)

        self.lbl_algoritmo = ttk.Label(self.frame, text="Algoritmo: --")
        self.lbl_algoritmo.pack()

        self.lbl_paso = ttk.Label(self.frame, text="Paso: 0")
        self.lbl_paso.pack()

        self.lbl_pagina = ttk.Label(self.frame, text="Página actual: --")
        self.lbl_pagina.pack()

        self.area_marcos = ttk.Frame(self.frame)
        self.area_marcos.pack(pady=10)

        self.celdas = []

        self.lbl_estado = ttk.Label(self.frame, text="Esperando resultados")
        self.lbl_estado.pack()

        controles = ttk.Frame(self.frame)
        controles.pack(pady=10)

        ttk.Button(controles, text="Anterior", command=self.anterior).grid(row=0, column=0, padx=5)
        self.btn_play = ttk.Button(controles, text="Play", command=self.play)
        self.btn_play.grid(row=0, column=1, padx=5)
        ttk.Button(controles, text="Siguiente", command=self.siguiente).grid(row=0, column=2, padx=5)

    def mostrar(self, resultado):
        self.resultado = resultado
        self.pasos = resultado["pasos"]
        self.indice = 0

        self.lbl_algoritmo.config(text="Algoritmo: " + resultado["algoritmo"])

        for widget in self.area_marcos.winfo_children():
            widget.destroy()

        self.celdas = []

        for i in range(resultado["num_marcos"]):
            celda = tk.Label(self.area_marcos, text="Vacío", width=10, height=3, bg="lightgray", relief="solid")
            celda.grid(row=0, column=i, padx=5)

            ttk.Label(self.area_marcos, text=f"Marco {i}").grid(row=1, column=i)

            self.celdas.append(celda)

        self.actualizar()

    def actualizar(self):
        paso = self.pasos[self.indice]

        self.lbl_paso.config(text=f"Paso: {self.indice + 1}/{len(self.pasos)}")
        self.lbl_pagina.config(text=f"Página actual: {paso['pagina']}")

        for i, celda in enumerate(self.celdas):
            valor = paso["marcos"][i]

            if valor is None:
                celda.config(text="Vacío", bg="lightgray")
            else:
                celda.config(text=str(valor), bg="lightgreen")

            if paso["fallo"] and i == paso["marco_afectado"]:
                if paso["reemplazada"] is not None:
                    celda.config(bg="orange")
                else:
                    celda.config(bg="tomato")

        if paso["fallo"]:
            if paso["reemplazada"] is not None:
                self.lbl_estado.config(text=f"Fallo: reemplazo de página {paso['reemplazada']}")
            else:
                self.lbl_estado.config(text="Fallo: marco libre utilizado")
        else:
            self.lbl_estado.config(text="Acierto: página en memoria")

    def siguiente(self):
        if self.indice < len(self.pasos) - 1:
            self.indice += 1
            self.actualizar()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.actualizar()

    def play(self):
        if self.reproduciendo:
            self.reproduciendo = False
            self.btn_play.config(text="Play")
        else:
            self.reproduciendo = True
            self.btn_play.config(text="Pausar")
            self.reproducir()

    def reproducir(self):
        if self.reproduciendo:
            if self.indice < len(self.pasos) - 1:
                self.siguiente()
                self.contenedor.after(1000, self.reproducir)
            else:
                self.reproduciendo = False
                self.btn_play.config(text="Play")


ventana = tk.Tk()
ventana.title("Simulador de Paginación")
ventana.geometry("600x350")

panel = PanelMarcos(ventana)

resultado = {
    "algoritmo": "FIFO",
    "num_marcos": 3,
    "cadena": [7, 0, 1, 2, 0, 3],
    "fallos": 5,
    "reemplazos": 2,
    "tasa_fallos": 0.833,
    "pasos": [
        {"paso": 0, "pagina": 7, "marcos": [7, None, None], "fallo": True, "reemplazada": None, "marco_afectado": 0},
        {"paso": 1, "pagina": 0, "marcos": [7, 0, None], "fallo": True, "reemplazada": None, "marco_afectado": 1},
        {"paso": 2, "pagina": 1, "marcos": [7, 0, 1], "fallo": True, "reemplazada": None, "marco_afectado": 2},
        {"paso": 3, "pagina": 2, "marcos": [2, 0, 1], "fallo": True, "reemplazada": 7, "marco_afectado": 0},
        {"paso": 4, "pagina": 0, "marcos": [2, 0, 1], "fallo": False, "reemplazada": None, "marco_afectado": None},
        {"paso": 5, "pagina": 3, "marcos": [2, 3, 1], "fallo": True, "reemplazada": 0, "marco_afectado": 1}
    ]
}

panel.mostrar(resultado)

ventana.mainloop()