import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox

import controlador as ctl
from visualizacion.panel_marcos import PanelMarcos


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de paginación y reemplazo de páginas")
        self.geometry("900x750")
        self.resultado = None
        self.cadena_actual = None
        self._construir()

    def _construir(self):
        f = ttk.LabelFrame(self, text="Configuración")
        f.pack(fill="x", padx=10, pady=5)

        ttk.Label(f, text="Algoritmo:").grid(row=0, column=0, padx=5, pady=5)
        self.var_alg = tk.StringVar(value="FIFO")
        ttk.Combobox(f, textvariable=self.var_alg, values=list(ctl.ALGORITMOS),
                     state="readonly", width=10).grid(row=0, column=1)

        ttk.Label(f, text="Marcos:").grid(row=0, column=2, padx=5)
        self.var_marcos = tk.IntVar(value=3)
        ttk.Spinbox(f, from_=1, to=20, textvariable=self.var_marcos,
                    width=5).grid(row=0, column=3)

        ttk.Label(f, text="Tipo de cadena:").grid(row=0, column=4, padx=5)
        self.var_tipo = tk.StringVar(value="Prueba del grupo")
        self.var_tipo.trace_add("write", lambda *_: setattr(self, "cadena_actual", None))
        ttk.Combobox(f, textvariable=self.var_tipo, values=ctl.TIPOS_CADENA,
                     state="readonly", width=16).grid(row=0, column=5)

        ttk.Label(f, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.var_cant = tk.IntVar(value=20)
        ttk.Spinbox(f, from_=1, to=200, textvariable=self.var_cant,
                    width=5).grid(row=1, column=1)
        ttk.Label(f, text="Página máx.:").grid(row=1, column=2)
        self.var_max = tk.IntVar(value=9)
        ttk.Spinbox(f, from_=1, to=50, textvariable=self.var_max,
                    width=5).grid(row=1, column=3)

        ttk.Label(f, text="Cadena manual (ej. 7,0,1,2):").grid(row=2, column=0,
                                                              columnspan=2, padx=5)
        self.var_manual = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_manual, width=50).grid(
            row=2, column=2, columnspan=4, sticky="we", pady=5)

        b = ttk.Frame(self)
        b.pack(fill="x", padx=10)
        ttk.Button(b, text="Generar", command=self.generar).pack(side="left", padx=5)
        ttk.Button(b, text="Ejecutar", command=self.ejecutar).pack(side="left", padx=5)
        ttk.Button(b, text="Comparar los 3", command=self.comparar).pack(side="left", padx=5)
        ttk.Button(b, text="Gráficos", command=self.graficos).pack(side="left", padx=5)
        ttk.Button(b, text="CSV tabla", command=self.csv_tabla).pack(side="left", padx=5)

        self.lbl_cadena = ttk.Label(self, text="Cadena: (sin generar)")
        self.lbl_cadena.pack(fill="x", padx=10, pady=2)

        self.lbl_res = ttk.Label(self, text="Sin resultados todavía.")
        self.lbl_res.pack(fill="x", padx=10, pady=5)

        marco_panel = ttk.LabelFrame(self, text="Evolución de los marcos")
        marco_panel.pack(fill="both", expand=True, padx=10, pady=5)
        self.panel = PanelMarcos(marco_panel)

        self._armar_csv_view()

        d = ttk.LabelFrame(self, text="Traducción de direcciones (estado final)")
        d.pack(fill="x", padx=10, pady=5)
        ttk.Label(d, text="Tamaño de página:").grid(row=0, column=0, padx=5, pady=5)
        self.var_tam = tk.IntVar(value=1024)
        ttk.Entry(d, textvariable=self.var_tam, width=8).grid(row=0, column=1)
        ttk.Label(d, text="Dirección lógica:").grid(row=0, column=2, padx=5)
        self.var_dir = tk.IntVar(value=0)
        ttk.Entry(d, textvariable=self.var_dir, width=10).grid(row=0, column=3)
        ttk.Button(d, text="Traducir", command=self.traducir).grid(row=0, column=4, padx=5)
        self.lbl_dir = ttk.Label(d, text="")
        self.lbl_dir.grid(row=0, column=5, padx=5)

    def _armar_csv_view(self):
        self.frm_csv = ttk.LabelFrame(self, text="Tabla de simulaciones (CSV)")
        self.frm_csv.pack(fill="both", expand=True, padx=10, pady=5)
        columns = ("algoritmo","num_marcos","tipo_cadena","largo_cadena","fallos","reemplazos","tasa_fallos")
        self.tree = ttk.Treeview(self.frm_csv, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col.replace("_"," ").title())
            self.tree.column(col, width=90)
        vsb = ttk.Scrollbar(self.frm_csv, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._ver_detalle)
        self._insertar_placeholder()

    def _insertar_placeholder(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert("", "end", values=("—", "—", "—", "—", "—", "—", "—"))

    def _cargar_csv_en_tree(self, filas):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for f in filas:
            tasa_pct = round(f["tasa_fallos"] * 100, 2)
            vals = [f.get(c,"") for c in ("algoritmo","num_marcos","tipo_cadena","largo_cadena","fallos","reemplazos","tasa_fallos")]
            vals[-1] = f"{tasa_pct}%"
            self.tree.insert("", "end", values=vals)

    def _ver_detalle(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        if not vals or vals[0] == "—":
            return
        self.var_alg.set(vals[0])
        self.var_marcos.set(int(vals[1]))
        self.var_tipo.set(vals[2])
        self.ejecutar()

    def _leer_cadena(self):
        if self.cadena_actual is not None and self.var_tipo.get() != "Manual":
            return self.cadena_actual
        cadena = ctl.generar_cadena(self.var_tipo.get(), self.var_manual.get(),
                                    self.var_cant.get(), self.var_max.get())
        self.cadena_actual = cadena
        self.lbl_cadena.config(text="Cadena: " + ", ".join(str(x) for x in cadena))
        return cadena

    def generar(self):
        self.cadena_actual = None
        try:
            self._leer_cadena()
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))

    def ejecutar(self):
        try:
            cadena = self._leer_cadena()
            self.resultado = ctl.ejecutar(self.var_alg.get(), cadena, self.var_marcos.get())
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return
        r = self.resultado
        self.lbl_res.config(text=(
            f"{r['algoritmo']} | fallos: {r['fallos']} | reemplazos: {r['reemplazos']} | tasa: {r['tasa_fallos'] * 100:.1f}%"))
        self.panel.mostrar(r)

    def comparar(self):
        try:
            filas = ctl.comparar(self._leer_cadena(), self.var_marcos.get())
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return
        txt = "\n".join(f"{n:<8} fallos={f:<3} reemplazos={r:<3} tasa={t * 100:.1f}%"
                        for n, f, r, t in filas)
        messagebox.showinfo("Comparación", txt)

    def graficos(self):
        try:
            from graficos import graficos as g
            cadena = self._leer_cadena()
            num_marcos = self.var_marcos.get()
        except ImportError:
            messagebox.showinfo("Gráficos", "El módulo de gráficos aún no está integrado.")
            return
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return
        g.mostrar(cadena, num_marcos)

    def csv_tabla(self):
        try:
            max_marcos = max(4, self.var_marcos.get())
            filas = ctl.generar_tabla_simulaciones(
                max_marcos=max_marcos,
                cantidad=self.var_cant.get(),
                max_pagina=self.var_max.get(),
            )
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return

        if not filas:
            messagebox.showwarning("CSV", "No se generaron resultados.")
            return

        cols = list(filas[0].keys())
        ruta = os.path.join("resultados", "simulaciones.csv")
        os.makedirs("resultados", exist_ok=True)
        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=cols)
                w.writeheader()
                w.writerows(filas)
        except OSError as e:
            messagebox.showerror("Error al guardar CSV", f"No se pudo escribir {ruta}:\n{e}")
            return

        self._cargar_csv_en_tree(filas)
        messagebox.showinfo("CSV guardado", f"{len(filas)} filas → {ruta}")

    def traducir(self):
        if not self.resultado:
            messagebox.showinfo("Traducción", "Primero ejecuta una simulación.")
            return
        try:
            dir_log = self.var_dir.get()
            tam = self.var_tam.get()
            pag, fis = ctl.traducir(self.resultado, dir_log, tam)
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return
        desp = dir_log % tam
        if fis is None:
            self.lbl_dir.config(text=f"Pág. {pag}, desp. {desp} -> FALLO DE PÁGINA (en disco)")
        else:
            marco = fis // tam
            self.lbl_dir.config(text=f"Pág. {pag}, desp. {desp}, marco {marco} -> física {fis}")


if __name__ == "__main__":
    App().mainloop()
