#No se como carajos vas hacer Sofia conectando esa mierda jaja
#Te dejare comentarios para que sepas que hace cada cosa, pero no te voy a explicar como funciona porque no tengo tiempo para eso jaja


class Optimo: 
    def __init__(self):

        #cuando se haga la simulación esto sera el nombre que aparecera
        self.nombre = "Optimo"


    def simular(self, cadena, num_marcos):
        
        # Verificar que la cantidad de marcos sea valida o en este caso positiva
           
        if type(num_marcos) is not int or num_marcos <= 0:
            raise ValueError("El número de marcos debe ser un entero positivo.")

        # Convertir en lista sin evitar modificar la entrada original
        if isinstance(cadena, (str, bytes)):
            raise ValueError("La cadena debe ser una secuencia de enteros")
        try:
            cadena = list(cadena)

        except TypeError as exc:
            raise ValueError("La cadena debe ser una secuencia de enteros") from exc
        if any(type(pagina) is not int or pagina < 0 for pagina in cadena):
            raise ValueError("La cadena debe ser una secuencia de enteros no negativos")

        # Representamos los marcos vacios con un none o nada es español creo que era así 

        marcos = [None] * num_marcos
        fallos = 0
        reemplazos = 0
        pasos = []

        for i, pagina in enumerate(cadena):
            fallo = False
            reemplazo = False
            marco_vacio = None

            # verificamos si la pagina esta en RAM 

            if pagina not in marcos:
                fallo = True
                fallos += 1

                if None in marcos:
                    #Se ocupa el primer marco vacio que se encuentre
                    posicion = marcos.index(None)
                else:
                    # Si la ram esta llena miramos cual es la pagina que se va a reemplazar, para eso buscamos la pagina que se va a usar mas adelante y la que no se use mas pronto sera la que se reemplace osea miramos el future 

                    futuras = cadena[i + 1:]
                    mayor_distancia = -1
                    posicion = -1

                    # Revisamos cada pagina almacenada en RAM 

                    for j, pagina_ram in enumerate(marcos):

                        if pagina_ram in futuras:
                            
                            distancia = futuras.index(pagina_ram)

                        else: 
                            # Esta página nunca volverá a usarse

                            distancia = float('inf')

                            # Elegimos la página cuyo próximo 
                            # uso esté más lejos en el futuro

                            if distancia > mayor_distancia:
                                mayor_distancia = distancia
                                posicion = j
                    # Se guardamos la pagina que fue reemplazada 
                    remplazada = marcos[posicion]
                    remplazo +=  1

                #Cargamos la pagina nueva 

                marcos[posicion] = pagina
                marcos_afectado = posicion

            # Guardamos una copia del estado de memoria 

            pasos.append({
                "paso": i,
                "pagina": pagina,
                "marcos": list(marcos),
                "fallo": fallo,
                "reemplazo": reemplazo,
                "marco_afectado": marcos_afectado
            })

        # Calculamos la tasa de falllos

        tasa_fallos = ( fallos / len(cadena) if cadena else 0.0 )

        # Devolvemos los resultados de la simulación

        return {
            "nombre": self.nombre,
            "num_marcos": num_marcos,
            "cadena": cadena,
            "fallos": fallos,
            "reemplazos": reemplazos,
            "tasa_fallos": tasa_fallos,
            "pasos": pasos
        }

#Ejcutar el algoritmo como una funcion
# chambea si has leido esto no le metiste chat y si le has medido chat va a estar bien jodido

def simular(cadena, num_marcos):
    return Optimo().simular(cadena, num_marcos)

                



        
                             



        