
# 1. Introducción

La memoria principal de una computadora es un recurso limitado, mientras que los programas actuales suelen requerir más memoria de la disponible físicamente. Para resolver este problema se emplea la memoria virtual, una técnica que permite a un proceso utilizar un espacio de direcciones lógicas mayor que la memoria física instalada, manteniendo en memoria únicamente las partes que necesita en cada momento y almacenando el resto en disco.

La técnica más utilizada para implementar la memoria virtual es la paginación. En este esquema, el espacio lógico del proceso se divide en bloques de igual tamaño denominados páginas, mientras que la memoria física se divide en marcos de página del mismo tamaño. Cuando un proceso intenta acceder a una página que no se encuentra cargada en memoria, ocurre un fallo de página, por lo que el sistema operativo debe recuperarla desde el almacenamiento secundario mediante un proceso de intercambio tambien llamado swapping.

Si todos los marcos disponibles están ocupados, el sistema operativo debe seleccionar una página para reemplazar. La estrategia utilizada para tomar esta decisión influye directamente en el rendimiento del sistema. Por ello existen distintos algoritmos de reemplazo de páginas, cada uno con ventajas y desventajas particulares.

En este proyecto se desarrolló un simulador en Python que reproduce el funcionamiento básico de la memoria virtual utilizando tres algoritmos de reemplazo: FIFO (First In, First Out),LRU (Least Recently Used) y Óptimo (Optimal Replacement). La aplicación permite configurar el número de marcos de memoria, generar o ingresar cadenas de referencia, calcular métricas de rendimiento y visualizar la evolución de los marcos durante la ejecución.

A través de esta simulación se busca responder la siguiente pregunta orientadora:

> **¿Cómo cambia el rendimiento de la memoria virtual cuando se modifica el número de marcos disponibles y el algoritmo de reemplazo utilizado?**

---

# 2. Objetivos

## 2.1 Objetivo general

Diseñar y desarrollar una aplicación en Python que simule la administración de memoria virtual mediante distintos algoritmos de reemplazo de páginas, con el fin de analizar y comparar su comportamiento al variar el número de marcos disponibles.

## 2.2 Objetivos específicos

- Implementar una memoria con un número configurable de marcos y un generador de cadenas de referencia de distintos tipos.

- Implementar los algoritmos de reemplazo FIFO, LRU y Óptimo utilizando un formato de salida común.

- Identificar los fallos de página y calcular métricas como número de fallos, tasa de fallos y cantidad de reemplazos realizados.

- Modelar la tabla de páginas, la traducción de direcciones lógicas a direcciones físicas y el mecanismo de intercambio entre memoria principal y disco.

- Comparar el comportamiento de los algoritmos mediante tablas y gráficos estadísticos.

- Mostrar visualmente la evolución de los marcos de memoria durante la simulación.

---
