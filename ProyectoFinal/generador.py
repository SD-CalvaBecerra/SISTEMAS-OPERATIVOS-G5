
import random

class GeneradorCadenas:
    def __init__(self):
        self.nombre = "Generador de cadenas"

    def generar_aleatoria(self, cantidad, max_pagina):
        cadena = []

        for i in range(cantidad):
            pagina = random.randint(0, max_pagina)
            cadena.append(pagina)

        return cadena
    
    def generar_localidad(self, cantidad, max_pagina):
        cadena = []
    
    def generar_belady(self):
        cadena = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        return cadena

        paginas_frecuentes = [0, 1, 2]

        for i in range(cantidad):
            if random.random() < 0.8:
                pagina = random.choice(paginas_frecuentes)
            else:
                pagina = random.randint(0, max_pagina)

            cadena.append(pagina)

        return cadena

