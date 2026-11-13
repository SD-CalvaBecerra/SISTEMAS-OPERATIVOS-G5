class Optimo: 
    def __init__(self):

        self.nombre = "Optimo"

    def simular(self, cadena, num_marcos):
           
        if type(num_marcos) is not int or num_marcos <= 0:
            raise ValueError("El número de marcos debe ser un entero positivo.")

        if isinstance(cadena, (str, bytes)):
            raise ValueError("La cadena debe ser una secuencia de enteros")
        try:
            cadena = list(cadena)

        except TypeError as exc:
            raise ValueError("La cadena debe ser una secuencia de enteros") from exc
        if any(type(pagina) is not int or pagina < 0 for pagina in cadena):
            raise ValueError("La cadena debe ser una secuencia de enteros no negativos")

        marcos = [None] * num_marcos
        fallos = 0
        reemplazos = 0
        pasos = []

        for i, pagina in enumerate(cadena):
            fallo = False
            reemplazo = False
            marco_vacio = None

            if pagina not in marcos:
                fallo = True
                fallos += 1

                if None in marcos:
                    posicion = marcos.index(None)
                else:

                    futuras = cadena[i + 1:]
                    mayor_distancia = -1
                    posicion = -1

                    for j, pagina_ram in enumerate(marcos):

                        if pagina_ram in futuras:
                            
                            distancia = futuras.index(pagina_ram)

                        else: 
                            distancia = float('inf')

                            if distancia > mayor_distancia:
                                mayor_distancia = distancia
                                posicion = j

                    remplazada = marcos[posicion]
                    remplazo +=  1

                marcos[posicion] = pagina
                marcos_afectado = posicion

            pasos.append({
                "paso": i,
                "pagina": pagina,
                "marcos": list(marcos),
                "fallo": fallo,
                "reemplazo": reemplazo,
                "marco_afectado": marcos_afectado
            })

        tasa_fallos = ( fallos / len(cadena) if cadena else 0.0 )

        return {
            "nombre": self.nombre,
            "num_marcos": num_marcos,
            "cadena": cadena,
            "fallos": fallos,
            "reemplazos": reemplazos,
            "tasa_fallos": tasa_fallos,
            "pasos": pasos
        }

def simular(cadena, num_marcos):
    return Optimo().simular(cadena, num_marcos)

                



        
                             



        