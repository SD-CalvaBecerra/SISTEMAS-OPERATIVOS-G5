#Acaba la segunda parte del código

class Metricas:

    #Aca el metodo constructutor recibe el resultado del algoritmo ( si me acuerdo de poo p no copie)

    def __init__(self, resultado):

        self.cadena = resultado["cadena"]
        self._pasos = resultado["pasos"]

    #calcular los fallos de pagina

    @property
    def  fallos(self):
        return sum(1 for paso in self._pasos if paso["fallo"])

    # Calcula cuantas páginas fueron reemplazadas

    @property
    def reemplazos(self):
        return sum(1 for paso in self._pasos if paso["reemplazada"] is not None)

    #calcular la tasa de fallos 
    @property
    def tasa_fallos(self):
        if not self._cadena:
            return 0.0

        return self.fallos / len(self._cadena)

    #Las metricas se devuelven en un diccionario 

    def calcular(self):
        return {
            "fallos": self.fallos,
            "reemplazos": self.reemplazos,
            "tasa_fallos": self.tasa_fallos
        }

# Metricas como funcion 

def calcular_metricas(resultado):
    return Metricas(resultado).calcular()