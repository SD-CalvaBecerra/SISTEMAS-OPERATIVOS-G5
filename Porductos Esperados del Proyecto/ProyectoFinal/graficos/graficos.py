import matplotlib.pyplot as plt
import controlador as ctl


def mostrar(cadena, num_marcos=3, max_marcos=7):
    """
    Muestra tres gráficos comparativos:
    1. Fallos vs. número de marcos (FIFO, LRU y Óptimo)
    2. Tasa de fallos (%) por algoritmo para `num_marcos`
    3. Anomalía de Belady en FIFO
    """
    if not cadena:
        return

    marcos_rango = list(range(1, max(4, max_marcos) + 1))
    fig, ejes = plt.subplots(1, 3, figsize=(15, 4.8))

    # 1. Fallos vs. número de marcos
    for nombre in ctl.ALGORITMOS:
        fallos = [ctl.ejecutar(nombre, cadena, m)["fallos"] for m in marcos_rango]
        ejes[0].plot(marcos_rango, fallos, marker="o", label=nombre)
    ejes[0].set_title("Fallos vs. Número de marcos")
    ejes[0].set_xlabel("Número de marcos")
    ejes[0].set_ylabel("Cantidad de fallos")
    ejes[0].set_xticks(marcos_rango)
    ejes[0].grid(True, linestyle="--", alpha=0.6)
    ejes[0].legend()

    # 2. Tasa de fallos (%) por algoritmo
    nombres = list(ctl.ALGORITMOS.keys())
    tasas = [ctl.ejecutar(n, cadena, num_marcos)["tasa_fallos"] * 100 for n in nombres]
    ejes[1].bar(nombres, tasas, color=["#e76f51", "#2a9d8f", "#264653"], edgecolor="black")
    ejes[1].set_title(f"Tasa de fallos ({num_marcos} marcos)")
    ejes[1].set_ylabel("Tasa de fallos (%)")
    ejes[1].set_ylim(0, 105)
    ejes[1].grid(axis="y", linestyle="--", alpha=0.6)
    for i, valor in enumerate(tasas):
        ejes[1].text(i, valor + 2, f"{valor:.1f}%", ha="center")

    # 3. Anomalía de Belady (FIFO)
    cadena_belady = ctl.generar_cadena("Belady")
    marcos_belady = [1, 2, 3, 4, 5, 6]
    fallos_belady = [ctl.ejecutar("FIFO", cadena_belady, m)["fallos"] for m in marcos_belady]
    ejes[2].plot(marcos_belady, fallos_belady, marker="s", color="#d62828", label="FIFO")
    ejes[2].annotate(
        "Anomalía (3→4 marcos)",
        xy=(4, fallos_belady[3]),
        xytext=(3.2, fallos_belady[3] + 1.2),
        arrowprops={"arrowstyle": "->", "color": "black"},
    )
    ejes[2].set_title("Anomalía de Belady (FIFO)")
    ejes[2].set_xlabel("Número de marcos")
    ejes[2].set_ylabel("Cantidad de fallos")
    ejes[2].set_xticks(marcos_belady)
    ejes[2].grid(True, linestyle="--", alpha=0.6)
    ejes[2].legend()

    plt.tight_layout()
    plt.show()
