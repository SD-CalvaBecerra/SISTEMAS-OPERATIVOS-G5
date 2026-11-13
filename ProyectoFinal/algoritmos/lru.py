class LRU:
    def __init__(self):
        self.nombre = "LRU"
 
    def simular(self, cadena, num_marcos):
        if not isinstance(num_marcos, int) or isinstance(num_marcos, bool) or num_marcos <= 0:
            raise ValueError("El número de marcos debe ser un entero mayor que 0")

        marcos = [None] * num_marcos
        ultimo_uso = {}
        fallos = 0
        reemplazos = 0
        pasos = []
        
        for i, pagina in enumerate(cadena):
            fallo = False
            reemplazada = None
            marco_afectado = None

            if pagina not in marcos:
                fallo = True
                fallos += 1
            
                if None in marcos:
                    posicion = marcos.index(None)
                    marcos[posicion] = pagina
                    marco_afectado = posicion
                  
                else:
                    reemplazada = min(marcos, key=lambda p: ultimo_uso[p])
                    posicion = marcos.index(reemplazada)
                    marcos[posicion] = pagina
                    reemplazos += 1
                    marco_afectado = posicion

            ultimo_uso[pagina] = i
            
            pasos.append({
                "paso": i,
                "pagina": pagina,
                "marcos": list(marcos),
                "fallo": fallo,
                "reemplazada": reemplazada,
                "marco_afectado": marco_afectado
            })
        
        tasa_fallos = fallos / len(cadena) if cadena else 0

        return {
            "algoritmo": self.nombre,
            "num_marcos": num_marcos,
            "cadena": cadena,
            "fallos": fallos,
            "reemplazos": reemplazos,
            "tasa_fallos": tasa_fallos,
            "pasos": pasos
        }

def simular(cadena, num_marcos):
    return LRU().simular(cadena, num_marcos)
