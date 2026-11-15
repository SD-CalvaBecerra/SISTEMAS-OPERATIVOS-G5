class MemoriaFisica:

    def __init__(self, num_marcos):
        if not isinstance(num_marcos, int) or isinstance(num_marcos, bool) or num_marcos <= 0:
            raise ValueError("El número de marcos debe ser mayor que 0")

        self.marcos = [None] * num_marcos

    def buscar_libre(self):
        if None in self.marcos:
            return self.marcos.index(None)
        return None

    def cargar_pagina(self, pagina, marco):
        if marco < 0 or marco >= len(self.marcos):
            raise ValueError("Marco inválido")

        if pagina in self.marcos:
            raise ValueError("La página ya está cargada")

        if self.marcos[marco] is not None:
            raise ValueError("El marco ya está ocupado")

        self.marcos[marco] = pagina

    def liberar_marco(self, marco):
        if marco < 0 or marco >= len(self.marcos):
            raise ValueError("Marco inválido")

        self.marcos[marco] = None
