import tkinter as tk
from tkinter import ttk, messagebox

import controlador as ctl

try:  
    from visualizacion.panel_marcos import PanelMarcos
except ImportError:
    try:
        from visualizacion import PanelMarcos
    except ImportError:
        PanelMarcos = None

class PanelBasico:
    def __init__(self, contenedor):
        self.texto = tk.Text(contenedor, height=14, font=("Courier", 10))
        self.texto.pack(fill="both", expand=True)

    def mostrar(self, resultado):
        n = resultado["num_marcos"]
        lineas = ["Pág  " + "  ".join(f"M{i}" for i in range(n)) + "  Estado"]
        for p in resultado["pasos"]:
            marcos = "  ".join(f"{'-' if m is None else m:>2}" for m in p["marcos"])
            estado = "FALLO" if p["fallo"] else "ok"
            if p["reemplazada"] is not None:
                estado += f" (sale {p['reemplazada']})"
            lineas.append(f"{p['pagina']:>3}  {marcos}  {estado}")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", "\n".join(lineas))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de paginación y reemplazo de páginas")
        self.geometry("900x700")
        self.resultado = None
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
        ttk.Button(b, text="Ejecutar", command=self.ejecutar).pack(side="left", padx=5)
        ttk.Button(b, text="Comparar los 3", command=self.comparar).pack(side="left", padx=5)
        ttk.Button(b, text="Gráficos", command=self.graficos).pack(side="left", padx=5)

        self.lbl_res = ttk.Label(self, text="Sin resultados todavía.")
        self.lbl_res.pack(fill="x", padx=10, pady=5)

        marco_panel = ttk.LabelFrame(self, text="Evolución de los marcos")
        marco_panel.pack(fill="both", expand=True, padx=10, pady=5)
        self.panel = (PanelMarcos or PanelBasico)(marco_panel)

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

    def _leer_cadena(self):
        return ctl.generar_cadena(self.var_tipo.get(), self.var_manual.get(),
                                  self.var_cant.get(), self.var_max.get())

    def ejecutar(self):
        try:
            cadena = self._leer_cadena()
            self.resultado = ctl.ejecutar(self.var_alg.get(), cadena, self.var_marcos.get())
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return
        r = self.resultado
        self.lbl_res.config(text=(
            f"{r['algoritmo']} | cadena: {r['cadena']} | fallos: {r['fallos']} | "
            f"reemplazos: {r['reemplazos']} | tasa: {r['tasa_fallos'] * 100:.1f}%"))
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
        except ImportError:
            messagebox.showinfo("Gráficos", "El módulo de gráficos aún no está integrado.")
            return
        g.mostrar(self._leer_cadena())

    def traducir(self):
        if not self.resultado:
            messagebox.showinfo("Traducción", "Primero ejecuta una simulación.")
            return
        try:
            pag, fis = ctl.traducir(self.resultado, self.var_dir.get(), self.var_tam.get())
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Error", str(e))
            return
        self.lbl_dir.config(text=f"Página {pag} -> " + (
            "FALLO DE PÁGINA" if fis is None else f"dirección física {fis}"))


if __name__ == "__main__":
    App().mainloop()
