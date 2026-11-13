
from controlador import comparar
from graficos.graficos import comparar_algoritmos

# Cadena de páginas para la simulación
cadena = [
    7, 0, 1, 2, 0, 3, 0, 4, 2, 3,
    0, 3, 2, 1, 2, 0, 1, 7, 0, 1
]

# Número de marcos de memoria
num_marcos = 3

# Ejecutar FIFO, LRU y Óptimo
resultados = comparar(cadena, num_marcos)

# Mostrar los resultados
for nombre, fallos, reemplazos, tasa in resultados:
    print(f"Algoritmo: {nombre}")
    print(f"Fallos: {fallos}")
    print(f"Reemplazos: {reemplazos}")
    print(f"Tasa de fallos: {tasa:.2%}")
    print("------------------------")

# Generar gráfico comparativo
comparar_algoritmos(resultados)
