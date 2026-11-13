class TablaPaginas:

    def __init__(self):
        self.tabla = {}

    
    def cargar_pagina(self, pagina, marco):

        if not isinstance(marco, int) or isinstance(marco, bool) or marco < 0:
            raise ValueError("El marco debe ser un entero no negativo")

        for pagina_actual, marco_actual in self.tabla.items():
            if marco_actual == marco and pagina_actual != pagina:
                raise ValueError("El marco ya está ocupado")

        self.tabla[pagina] = marco


    def buscar_pagina(self, pagina):
        return self.tabla.get(pagina)

    def eliminar_pagina(self, pagina):
        if pagina in self.tabla:
            del self.tabla[pagina]
