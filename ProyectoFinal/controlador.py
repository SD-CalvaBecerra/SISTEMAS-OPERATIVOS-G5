from algoritmos.fifo import FIFO
from algoritmos.lru import LRU
from algoritmos.optimo import Optimo
from generador import GeneradorCadenas
from metricas import calcular_metricas
from validador import validar_resultado
from direcciones.tabla_paginas import TablaPaginas
from direcciones.traductor import TraductorDirecciones

ALGORITMOS = {"FIFO": FIFO().simular, "LRU": LRU().simular, "Óptimo": Optimo().simular}
TIPOS_CADENA = ["Manual", "Aleatoria", "Con localidad", "Belady", "Prueba del grupo"]

def parsear_cadena(texto):
    partes = texto.replace(",", " ").split()
    if not partes:
        raise ValueError("La cadena está vacía")
    try:
        cadena = [int(p) for p in partes]
    except ValueError:
        raise ValueError("La cadena solo admite números enteros")
    if any(p < 0 for p in cadena):
        raise ValueError("Las páginas no pueden ser negativas")
    return cadena

def generar_cadena(tipo, texto="", cantidad=20, max_pagina=9):
    g = GeneradorCadenas()
    if tipo == "Manual":
        return parsear_cadena(texto)
    if tipo == "Aleatoria":
        return g.generar_aleatoria(cantidad, max_pagina)
    if tipo == "Con localidad":
        return g.generar_localidad(cantidad, max_pagina)
    if tipo == "Belady":
        return g.generar_belady()
    if tipo == "Prueba del grupo":
        return g.generar_prueba()
    raise ValueError(f"Tipo de cadena desconocido: {tipo}")

def ejecutar(algoritmo, cadena, num_marcos):
    resultado = ALGORITMOS[algoritmo](list(cadena), num_marcos)
    validar_resultado(resultado)
    return resultado

def comparar(cadena, num_marcos):
    filas = []
    for nombre in ALGORITMOS:
        m = calcular_metricas(ejecutar(nombre, cadena, num_marcos))
        filas.append((nombre, m["fallos"], m["reemplazos"], m["tasa_fallos"]))
    return filas

def traducir(resultado, direccion_logica, tamano_pagina):
    if tamano_pagina <= 0:
        raise ValueError("El tamaño de página debe ser mayor que 0")
    tabla = TablaPaginas()
    for marco, pagina in enumerate(resultado["pasos"][-1]["marcos"] if resultado["pasos"] else []):
        if pagina is not None:
            tabla.cargar_pagina(pagina, marco)
    pagina = direccion_logica // tamano_pagina
    fisica = TraductorDirecciones(tabla, tamano_pagina).traducir(direccion_logica)
    return pagina, fisica
