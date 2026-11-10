
from algoritmos.lru import LRU
from graficos.graficos import comparar_algoritmos, grafico_fallos_dinamico

# Cadena de prueba compartida
cadena = [
    7, 0, 1, 2, 0, 3, 0, 4, 2, 3,
    0, 3, 2, 1, 2, 0, 1, 7, 0, 1
]

# Ejecutamos el algoritmo LRU
lru = LRU()
resultado_lru = lru.simular(cadena, 3)

# Mostramos los resultados
print("Algoritmo:", resultado_lru["algoritmo"])
print("Fallos:", resultado_lru["fallos"])
print("Tasa:", resultado_lru["tasa_fallos"])

# Creamos una lista con los resultados disponibles
resultados = [resultado_lru]

# Generamos el gráfico automáticamente
comparar_algoritmos(resultados)


# Prueba del gráfico dinámico con LRU
algoritmos = {
    "LRU": LRU()
}

marcos = [2, 3, 4, 5]

grafico_fallos_dinamico(cadena, algoritmos, marcos)
