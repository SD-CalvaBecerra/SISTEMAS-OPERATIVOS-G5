
import matplotlib.pyplot as plt


# GRÁFICO 1: Fallos vs. número de marcos
def grafico_fallos_marcos(marcos, fifo, lru, optimo):
    plt.figure(figsize=(8, 5))

    plt.plot(marcos, fifo, marker="o", label="FIFO")
    plt.plot(marcos, lru, marker="s", label="LRU")
    plt.plot(marcos, optimo, marker="^", label="Óptimo")

    plt.title("Fallos de página vs. número de marcos")
    plt.xlabel("Número de marcos")
    plt.ylabel("Cantidad de fallos de página")

    plt.xticks(marcos)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# GRÁFICO 2: Tasa de fallos por algoritmo
def grafico_tasa_fallos(tasas):
    algoritmos = list(tasas.keys())
    porcentajes = [tasa * 100 for tasa in tasas.values()]

    plt.figure(figsize=(8, 5))

    barras = plt.bar(
        algoritmos,
        porcentajes,
        color=["royalblue", "orange", "seagreen"]
    )

    plt.title("Tasa de fallos por algoritmo")
    plt.xlabel("Algoritmos")
    plt.ylabel("Tasa de fallos (%)")
    plt.ylim(0, 100)

    for barra, porcentaje in zip(barras, porcentajes):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 1,
            f"{porcentaje:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    plt.show()


# GRÁFICO 3: Anomalía de Belady
def grafico_belady(marcos, fallos):
    plt.figure(figsize=(8, 5))

    plt.plot(
        marcos,
        fallos,
        marker="o",
        color="red",
        linewidth=2,
        label="FIFO"
    )

    plt.title("Anomalía de Belady - Algoritmo FIFO")
    plt.xlabel("Número de marcos")
    plt.ylabel("Cantidad de fallos de página")

    plt.xticks(marcos)
    plt.ylim(bottom=0)
    plt.grid(True)
    plt.legend()

    for x, y in zip(marcos, fallos):
        plt.annotate(
            str(y),
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center"
        )

    plt.tight_layout()
    plt.show()



# GRÁFICO DINÁMICO: Fallos según número de marcos
def grafico_fallos_dinamico(cadena, algoritmos, marcos):
    """
    Ejecuta los algoritmos con diferentes cantidades
    de marcos y representa sus fallos de página.

    algoritmos: diccionario con nombre y objeto del algoritmo.
    """

    plt.figure(figsize=(8, 5))

    for nombre, algoritmo in algoritmos.items():
        fallos = []

        for num_marcos in marcos:
            resultado = algoritmo.simular(cadena, num_marcos)
            fallos.append(resultado["fallos"])

        plt.plot(marcos, fallos, marker="o", label=nombre)

    plt.title("Fallos de página vs. número de marcos")
    plt.xlabel("Número de marcos")
    plt.ylabel("Cantidad de fallos de página")
    plt.xticks(marcos)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# CONEXIÓN CON LOS RESULTADOS DEL SIMULADOR

def comparar_algoritmos(resultados):
    """
    Recibe una lista de resultados de FIFO, LRU y Óptimo.
    Cada resultado debe respetar el formato del proyecto.
    """

    tasas = {}

    for resultado in resultados:
        nombre = resultado["algoritmo"]
        tasa = resultado["tasa_fallos"]

        tasas[nombre] = tasa

    grafico_tasa_fallos(tasas)


# ANOMALÍA DE BELADY CON FIFO REAL
def grafico_belady_dinamico(algoritmo_fifo):
    cadena_belady = [
        1, 2, 3, 4, 1, 2,
        5, 1, 2, 3, 4, 5
    ]

    marcos = [3, 4]
    fallos = []

    for cantidad in marcos:
        resultado = algoritmo_fifo.simular(
            cadena_belady, cantidad
        )
        fallos.append(resultado["fallos"])

    grafico_belady(marcos, fallos)

    if fallos[1] > fallos[0]:
        print("Se detectó la anomalía de Belady.")
    else:
        print("No se detectó la anomalía de Belady.")


# DATOS DE PRUEBA
if __name__ == "__main__":

    marcos = [2, 3, 4, 5]
    fifo = [17, 15, 12, 10]
    lru = [16, 12, 10, 8]
    optimo = [13, 9, 8, 7]

    grafico_fallos_marcos(marcos, fifo, lru, optimo)

    tasas = {
        "FIFO": 0.75,
        "LRU": 0.60,
        "Óptimo": 0.45
    }

    grafico_tasa_fallos(tasas)

# Ejemplo clásico de la anomalía de Belady
    marcos_belady = [3, 4]
    fallos_belady = [9, 10]

    grafico_belady(marcos_belady, fallos_belady)
