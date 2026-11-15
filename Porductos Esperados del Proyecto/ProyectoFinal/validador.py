CLAVES = ("algoritmo", "num_marcos", "cadena", "fallos", "reemplazos",
          "tasa_fallos", "pasos")
CLAVES_PASO = ("paso", "pagina", "marcos", "fallo", "reemplazada",
               "marco_afectado")


def validar_resultado(resultado):
    if not isinstance(resultado, dict):
        raise ValueError("El resultado debe ser un diccionario")
    for clave in CLAVES:
        if clave not in resultado:
            raise ValueError(f"Falta la clave '{clave}'")

    n = resultado["num_marcos"]
    cadena = resultado["cadena"]
    pasos = resultado["pasos"]
    if len(pasos) != len(cadena):
        raise ValueError("Debe haber un paso por cada página de la cadena")

    for i, paso in enumerate(pasos):
        for clave in CLAVES_PASO:
            if clave not in paso:
                raise ValueError(f"Paso {i}: falta la clave '{clave}'")
        if len(paso["marcos"]) != n:
            raise ValueError(f"Paso {i}: 'marcos' debe tener {n} posiciones")
        if paso["pagina"] != cadena[i]:
            raise ValueError(f"Paso {i}: la página no coincide con la cadena")
        if not paso["fallo"] and (paso["reemplazada"] is not None
                                  or paso["marco_afectado"] is not None):
            raise ValueError(f"Paso {i}: un acierto no puede tener reemplazo")

    fallos = sum(1 for p in pasos if p["fallo"])
    reemplazos = sum(1 for p in pasos if p["reemplazada"] is not None)
    if resultado["fallos"] != fallos:
        raise ValueError("'fallos' no coincide con los pasos")
    if resultado["reemplazos"] != reemplazos:
        raise ValueError("'reemplazos' no coincide con los pasos")
    esperada = fallos / len(cadena) if cadena else 0
    if abs(resultado["tasa_fallos"] - esperada) > 1e-9:
        raise ValueError("'tasa_fallos' no coincide con fallos/len(cadena)")
    return True
