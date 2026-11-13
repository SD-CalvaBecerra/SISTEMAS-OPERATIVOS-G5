class Metricas:

    def __init__(self, resultado):
        self._cadena = resultado["cadena"]
        self._pasos = resultado["pasos"]

    @property
    def fallos(self):
        return sum(1 for paso in self._pasos if paso["fallo"])

    @property
    def reemplazos(self):
        return sum(1 for paso in self._pasos if paso["reemplazada"] is not None)

    @property
    def tasa_fallos(self):
        if not self._cadena:
            return 0.0
        return self.fallos / len(self._cadena)

    def calcular(self):
        return {
            "fallos": self.fallos,
            "reemplazos": self.reemplazos,
            "tasa_fallos": self.tasa_fallos,
        }

def calcular_metricas(resultado):
    return Metricas(resultado).calcular()
