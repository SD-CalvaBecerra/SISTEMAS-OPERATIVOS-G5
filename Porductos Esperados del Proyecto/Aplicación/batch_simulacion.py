import os
import pandas as pd
from controlador import generar_tabla_simulaciones


def batch_simulacion():
    """
    Repite la simulación con distintos datos y guarda cada resultado como una fila.
    Columnas: algoritmo, num_marcos, tipo_cadena, largo_cadena, fallos, reemplazos, tasa_fallos
    """
    os.makedirs("resultados", exist_ok=True)
    filas = generar_tabla_simulaciones(max_marcos=7, cantidad=20, max_pagina=9)
    df = pd.DataFrame(filas)
    ruta = os.path.join("resultados", "simulaciones.csv")
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Listo. {len(filas)} filas guardadas en {ruta}")
    return df


if __name__ == "__main__":
    datos = batch_simulacion()
    print("\nVista rápida:")
    print(datos.head(15).to_string(index=False))
