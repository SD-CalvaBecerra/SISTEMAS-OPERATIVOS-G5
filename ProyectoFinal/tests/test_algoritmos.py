import unittest
from algoritmos.fifo import FIFO
from algoritmos.lru import LRU
from algoritmos.optimo import Optimo
from validador import validar_resultado
import controlador

class TestAlgoritmos(unittest.TestCase):

    def test_fifo(self):
        fifo = FIFO()

        cadena = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3,
                  0, 3, 2, 1, 2, 0, 1, 7, 0, 1]

        resultado = fifo.simular(cadena, 3)

        self.assertEqual(resultado["fallos"], 15)
        self.assertEqual(resultado["reemplazos"], 12)

    def test_lru(self):
        lru = LRU()

        cadena = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3,
                  0, 3, 2, 1, 2, 0, 1, 7, 0, 1]

        resultado = lru.simular(cadena, 3)

        self.assertEqual(resultado["fallos"], 12)
        self.assertEqual(resultado["reemplazos"], 9)
   
    def test_cadena_vacia(self):
        fifo = FIFO()
        lru = LRU()

        resultado_fifo = fifo.simular([], 3)
        resultado_lru = lru.simular([], 3)

        self.assertEqual(resultado_fifo["fallos"], 0)
        self.assertEqual(resultado_lru["fallos"], 0)
    
    def test_marcos_invalidos(self):
        fifo = FIFO()
        lru = LRU()

        with self.assertRaises(ValueError):
            fifo.simular([1, 2, 3], 0)

        with self.assertRaises(ValueError):
            lru.simular([1, 2, 3], 0)
    
    def test_sin_reemplazos(self):
        fifo = FIFO()
        lru = LRU()

        cadena = [1, 2, 3, 1, 2, 3]

        resultado_fifo = fifo.simular(cadena, 3)
        resultado_lru = lru.simular(cadena, 3)

        self.assertEqual(resultado_fifo["fallos"], 3)
        self.assertEqual(resultado_fifo["reemplazos"], 0)

        self.assertEqual(resultado_lru["fallos"], 3)
        self.assertEqual(resultado_lru["reemplazos"], 0)

    def test_optimo(self):
        cadena = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3,
                  0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
        r = Optimo().simular(cadena, 3)
        self.assertEqual(r["fallos"], 9)
        self.assertEqual(r["reemplazos"], 6)

    def test_formato_valido(self):
        cadena = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3]
        for alg in (FIFO(), LRU(), Optimo()):
            self.assertTrue(validar_resultado(alg.simular(cadena, 3)))

    def test_belady(self):
        from generador import GeneradorCadenas
        c = GeneradorCadenas().generar_belady()
        self.assertEqual(FIFO().simular(c, 3)["fallos"], 9)
        self.assertEqual(FIFO().simular(c, 4)["fallos"], 10)

    def test_controlador(self):
        self.assertEqual(controlador.parsear_cadena("1, 2 3"), [1, 2, 3])
        with self.assertRaises(ValueError):
            controlador.parsear_cadena("a,b")
        filas = controlador.comparar(controlador.generar_cadena("Prueba del grupo"), 3)
        self.assertEqual([f[1] for f in filas], [15, 12, 9])
        r = controlador.ejecutar("FIFO", [1, 2, 3], 3)
        self.assertEqual(controlador.traducir(r, 1030, 1024), (1, 6))

    def test_tabla_simulaciones(self):
        filas = controlador.generar_tabla_simulaciones(max_marcos=4)
        self.assertTrue(len(filas) > 0)
        for f in filas:
            self.assertGreaterEqual(f["tasa_fallos"], 0.0)
            self.assertLessEqual(f["tasa_fallos"], 1.0)

    def test_direcciones_y_swapping(self):
        from direcciones.memoria_fisica import MemoriaFisica
        from direcciones.swapping import Swapping
        from direcciones.tabla_paginas import TablaPaginas
        from direcciones.traductor import TraductorDirecciones

        mem = MemoriaFisica(2)
        marco = mem.buscar_libre()
        self.assertEqual(marco, 0)
        mem.cargar_pagina(5, marco)
        self.assertEqual(mem.buscar_libre(), 1)

        swap = Swapping()
        swap.guardar_pagina(5, "datos_p5")
        self.assertEqual(swap.recuperar_pagina(5), "datos_p5")
        swap.eliminar_pagina(5)
        self.assertIsNone(swap.recuperar_pagina(5))

        tabla = TablaPaginas()
        tabla.cargar_pagina(5, 0)
        trad = TraductorDirecciones(tabla, 1024)
        self.assertEqual(trad.traducir(5 * 1024 + 120), 120)
        self.assertIsNone(trad.traducir(2 * 1024 + 10))

if __name__ == "__main__":
    unittest.main()
