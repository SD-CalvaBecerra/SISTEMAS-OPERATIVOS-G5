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
# 3. Marco teórico

## 3.1. Memoria virtual

La memoria virtual es una técnica de administración de memoria que permite ejecutar procesos sin necesidad de mantenerlos completamente cargados en la memoria principal (RAM). Mediante esta técnica, un programa puede utilizar un espacio de direcciones virtuales mayor que la memoria física disponible, mientras el sistema operativo mantiene en RAM las partes que necesita y utiliza el almacenamiento secundario como respaldo.

Su utilización responde a la necesidad de ejecutar programas de gran tamaño y mantener varios procesos activos al mismo tiempo. En muchos casos, un programa no necesita acceder a todas sus instrucciones y datos de forma simultánea. Por ello, mantener únicamente las partes utilizadas puede favorecer el aprovechamiento de la memoria principal y la multiprogramación.

La memoria virtual requiere mecanismos para relacionar las direcciones que utiliza un programa con las posiciones reales de la memoria física. Una de las técnicas más utilizadas para conseguirlo es la paginación (Tanenbaum, 2009; Burga Montañez, 2026).

## 3.2. Paginación de memoria

La paginación es una técnica que divide el espacio de direcciones virtuales de un proceso en bloques de tamaño fijo, llamados páginas, y la memoria física en bloques del mismo tamaño, denominados marcos de página. Las páginas pueden ubicarse en marcos no contiguos de la RAM, por lo que un proceso no necesita ocupar una única región continua de memoria física.

La correspondencia entre una página virtual y un marco físico se mantiene mediante una tabla de páginas. Cuando una página requerida no está presente en la RAM, el sistema operativo debe gestionar su incorporación, siempre que el acceso sea válido.

### 3.2.1. Páginas y marcos de página

- **Página:** bloque de tamaño fijo que pertenece al espacio de direcciones virtuales del proceso.
- **Marco de página:** bloque de memoria física en el que puede cargarse una página.
- **Cadena de referencias:** secuencia de páginas que un programa solicita durante su ejecución. Es la entrada utilizada para estudiar el comportamiento de los algoritmos de reemplazo.

El tamaño de una página y el de un marco deben coincidir dentro de un mismo esquema de paginación. De esta forma, una página puede cargarse en cualquiera de los marcos disponibles.

### 3.2.2. Tabla de páginas y unidad de manejo de memoria (MMU)

La tabla de páginas registra la relación entre las páginas virtuales y sus correspondientes marcos en memoria física. También puede contener información de control, como la presencia o ausencia de una página, los permisos de acceso y los indicadores de modificación o referencia.

La unidad de manejo de memoria (MMU) es el componente de hardware que interviene en la traducción de direcciones virtuales a direcciones físicas. Cuando un programa genera una dirección virtual, la MMU utiliza la información de la tabla de páginas para determinar la dirección física correspondiente.

### 3.2.3. Traducción de direcciones virtuales a físicas

Una dirección virtual se divide en dos componentes:

- **Número de página:** identifica la página virtual a la que se desea acceder.
- **Desplazamiento (*offset*):** señala la posición dentro de esa página.

El número de página permite consultar la tabla de páginas y obtener el marco físico asociado. Si la página está presente, el desplazamiento se conserva para construir la dirección física.

La relación puede expresarse de la siguiente forma:

$$
\text{Dirección física} = (\text{Número de marco} \times \text{Tamaño de página}) + \text{Desplazamiento}
$$

Si la página no está presente, no se puede realizar la traducción directamente y debe atenderse el fallo de página.

## 3.3. Fallos de página y reemplazo de páginas

Un acierto de página ocurre cuando la página solicitada ya se encuentra cargada en la memoria física. En cambio, un fallo de página ocurre cuando se intenta acceder a una página que no está presente en RAM. En un sistema operativo real, el acceso debe comprobarse y, si es válido, se gestiona la recuperación de la página necesaria.

Cuando sucede un fallo de página, pueden presentarse dos situaciones:

1. **Existe un marco libre:** la página solicitada se carga en ese espacio sin desalojar otra página.
2. **Todos los marcos están ocupados:** se necesita seleccionar una página para reemplazarla y liberar espacio para la nueva.

Cuando se desaloja una página modificada, puede ser necesario escribir su contenido actualizado en el almacenamiento secundario. Si no se modificó y existe una copia válida, esa escritura puede evitarse.

### 3.3.1. Intercambio de páginas (*swapping*)

El intercambio entre memoria principal y almacenamiento secundario permite retirar información de la RAM y recuperarla cuando sea necesaria. En este proyecto, el simulador representa de manera simplificada las páginas que salen de los marcos y su paso al almacenamiento secundario. Esta representación permite visualizar el reemplazo, aunque no reproduce todas las operaciones de un sistema operativo real.

## 3.4. Algoritmos de reemplazo de páginas

Los algoritmos de reemplazo de páginas establecen qué página debe abandonar la memoria cuando ocurre un fallo y no existen marcos libres. Su objetivo es administrar el espacio disponible y evitar, en la medida de lo posible, fallos futuros innecesarios.

Existen diferentes estrategias. Para este proyecto se seleccionaron los algoritmos FIFO, LRU y Óptimo, porque permiten comparar criterios de reemplazo basados en el orden de llegada, el uso reciente y el conocimiento de referencias futuras.

### 3.4.1. FIFO (*First In, First Out*)

El algoritmo FIFO, o *primero en entrar, primero en salir*, reemplaza la página que lleva más tiempo almacenada en la memoria. Para ello, considera el orden de llegada de las páginas: la primera que ingresó será la primera candidata a salir cuando se necesite liberar un marco.

Su principal ventaja es la sencillez de su funcionamiento. Sin embargo, no tiene en cuenta si una página se utiliza con frecuencia. En consecuencia, puede desalojar una página importante simplemente porque fue la primera en cargarse.

### 3.4.2. LRU (*Least Recently Used*)

El algoritmo LRU, o *menos recientemente utilizado*, selecciona para reemplazo la página que lleva más tiempo sin utilizarse. A diferencia de FIFO, no se basa en el momento de llegada de la página, sino en cuándo se realizó su última referencia.

Este algoritmo parte de la idea de que las páginas utilizadas recientemente tienen cierta probabilidad de volver a necesitarse. Cuando una página es solicitada y ya está en memoria, se actualiza la información de su último uso. Si ocurre un fallo y todos los marcos están ocupados, se reemplaza la página cuya última utilización es más antigua.

Entre sus ventajas se encuentra el aprovechamiento de la localidad temporal, lo que puede reducir los fallos respecto de FIFO para determinadas cadenas de referencias. No obstante, necesita registrar el uso de las páginas, puede requerir más recursos para su implementación y no garantiza siempre la menor cantidad posible de fallos.

### 3.4.3. Algoritmo Óptimo (*Optimal Page Replacement*)

El algoritmo Óptimo reemplaza la página cuyo próximo uso ocurrirá más lejos en el futuro o que no volverá a utilizarse. Con este criterio, busca obtener la cantidad mínima de fallos de página posible para una cadena de referencias y un número de marcos determinados.

Su principal limitación es que requiere conocer anticipadamente las solicitudes futuras, información que un sistema operativo normalmente no posee. Por ello, se utiliza principalmente como una referencia teórica para evaluar el rendimiento de otros algoritmos y como criterio de comparación en simulaciones.

## 3.5. Conceptos para evaluar los algoritmos

### 3.5.1. Localidad temporal

El principio de localidad temporal establece que, cuando un programa accede a una página, existe la posibilidad de que vuelva a utilizarla en un periodo cercano. Este comportamiento es especialmente relevante para LRU, porque favorece la conservación de páginas utilizadas recientemente.

### 3.5.2. Métricas de rendimiento

Para comparar el comportamiento de los algoritmos se utilizan los siguientes indicadores:

- **Fallos de página:** cantidad de referencias a páginas que no estaban cargadas en los marcos.
- **Aciertos de página:** cantidad de referencias a páginas que sí estaban presentes.
- **Reemplazos:** cantidad de ocasiones en que se desaloja una página para cargar otra cuando la memoria está llena.
- **Tasa de fallos:** proporción de referencias que producen fallos de página.

La tasa de fallos se calcula mediante:

$$
\text{Tasa de fallos (\%)} = \frac{\text{Número de fallos de página}}{\text{Total de referencias}} \times 100
$$

Estas métricas permiten comparar algoritmos bajo las mismas condiciones, utilizando una cadena de referencias y una cantidad de marcos determinadas.

### 3.5.3. Anomalía de Belady

La anomalía de Belady es el fenómeno por el cual un algoritmo de reemplazo puede producir más fallos de página al aumentar el número de marcos disponibles. Este comportamiento puede presentarse en FIFO, por lo que disponer de más memoria no siempre implica una reducción de fallos con ese algoritmo.

En el proyecto se utiliza una cadena específica para mostrar este fenómeno. La demostración numérica y su gráfica se presentarán en la sección de resultados, separadas del ejemplo principal utilizado para comparar FIFO, LRU y Óptimo.
