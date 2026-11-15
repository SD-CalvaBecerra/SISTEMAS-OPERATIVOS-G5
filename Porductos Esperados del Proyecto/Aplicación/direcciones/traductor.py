class TraductorDirecciones:

    def __init__(self, tabla_paginas, tamano_pagina):
        self.tabla_paginas = tabla_paginas
        self.tamano_pagina = tamano_pagina

    def traducir(self, direccion_logica):
        if direccion_logica < 0:
            raise ValueError("La dirección lógica no puede ser negativa")

        pagina = direccion_logica // self.tamano_pagina
        desplazamiento = direccion_logica % self.tamano_pagina

        marco = self.tabla_paginas.buscar_pagina(pagina)

        if marco is None:
            return None

        direccion_fisica = marco * self.tamano_pagina + desplazamiento

        return direccion_fisica
