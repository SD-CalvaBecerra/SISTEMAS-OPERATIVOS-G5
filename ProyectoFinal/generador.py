import random

class GeneradorCadenas:
    def __init__(self):
        self.nombre = "Generador de cadenas"

    def generar_aleatoria(self, cantidad, max_pagina):
        return [random.randint(0, max_pagina) for _ in range(cantidad)]

    def generar_localidad(self, cantidad, max_pagina):
        frecuentes = list(range(min(3, max_pagina + 1)))
        cadena = []
        for _ in range(cantidad):
            if random.random() < 0.8:
                cadena.append(random.choice(frecuentes))
            else:
                cadena.append(random.randint(0, max_pagina))
        return cadena

    def generar_belady(self):
        return [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

    def generar_prueba(self):
        return [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
