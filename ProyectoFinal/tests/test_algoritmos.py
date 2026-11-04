
import unittest
from algoritmos.fifo import FIFO
from algoritmos.lru import LRU


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


if __name__ == "__main__":
    unittest.main()
