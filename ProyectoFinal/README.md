# Simulador de paginación y reemplazo de páginas

Algoritmos: FIFO, LRU y Óptimo. Interfaz en Tkinter.

## Instalar y ejecutar
```
pip install -r requirements.txt
python main.py
python -m unittest discover      # pruebas
```
Tkinter viene con Python (en Linux: `sudo apt install python3-tk`).

## Formato de entrada
- `cadena`: lista de enteros no negativos, ej. `[7, 0, 1, 2, 0, 3]`
- `num_marcos`: entero mayor que 0
- Todos los algoritmos exponen `simular(cadena, num_marcos)`.

## Formato de salida (diccionario)
`algoritmo, num_marcos, cadena, fallos, reemplazos, tasa_fallos (0 a 1), pasos`.
Cada paso: `paso, pagina, marcos (None = vacío), fallo, reemplazada, marco_afectado`.
`validar_resultado(resultado)` en `validador.py` comprueba el formato.

## Estructura
- `main.py` ventana principal · `controlador.py` lógica sin interfaz
- `algoritmos/` fifo, lru, optimo · `generador.py` · `metricas.py` · `validador.py`
- `direcciones/` tabla de páginas, traductor, swapping
- `visualizacion/panel_marcos.py` → `PanelMarcos(contenedor).mostrar(resultado)` (Persona 5)
- `graficos/graficos.py` → función `mostrar(cadena)` (Persona 6)
- `tests/` · `informe/`

Cadena de prueba del grupo (3 marcos): FIFO 15, LRU 12, Óptimo 9 fallos.
