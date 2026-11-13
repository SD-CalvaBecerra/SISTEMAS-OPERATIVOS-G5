class Swapping:

    def __init__(self):
        self.disco = {}

    def guardar_pagina(self, pagina, contenido):
        self.disco[pagina] = contenido

    def recuperar_pagina(self, pagina):
        return self.disco.get(pagina)

    def eliminar_pagina(self, pagina):
        if pagina in self.disco:
            del self.disco[pagina]
