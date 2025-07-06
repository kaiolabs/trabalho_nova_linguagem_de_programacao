"""
Testes para o módulo de teoria musical da MelodyScript.
"""

import sys
import unittest
from pathlib import Path

# Adicionar o diretório raiz ao path para permitir importações relativas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.teoria_musical import (
    calcular_duracao,
    calcular_frequencia,
    calcular_frequencias_acorde,
    indice_para_frequencia,
    nota_para_indice,
)


class TestTeoriaMusical(unittest.TestCase):
    """Testes para as funções de teoria musical."""

    def test_calcular_duracao(self):
        """Testa o cálculo de duração de notas."""
        # Tempo = 60 BPM (1 batida por segundo)
        self.assertEqual(calcular_duracao("minima", 60), 2.0)
        self.assertEqual(calcular_duracao("seminima", 60), 1.0)
        self.assertEqual(calcular_duracao("colcheia", 60), 0.5)

        # Tempo = 120 BPM (2 batidas por segundo)
        self.assertEqual(calcular_duracao("minima", 120), 1.0)
        self.assertEqual(calcular_duracao("seminima", 120), 0.5)
        self.assertEqual(calcular_duracao("colcheia", 120), 0.25)

    def test_calcular_frequencia(self):
        """Testa o cálculo de frequência de notas."""
        # Notas naturais
        self.assertAlmostEqual(calcular_frequencia("la"), 440.0)
        self.assertAlmostEqual(calcular_frequencia("do"), 261.63, delta=0.01)

        # Notas com modificadores
        self.assertAlmostEqual(calcular_frequencia("la", "#"), 440.0 * 1.059463, delta=0.01)
        self.assertAlmostEqual(calcular_frequencia("si", "b"), 493.88 * 0.943874, delta=0.01)

    def test_calcular_frequencias_acorde(self):
        """Testa o cálculo de frequências para acordes."""
        # Acorde de Do maior (do-mi-sol)
        frequencias = calcular_frequencias_acorde("do", "maior")
        self.assertEqual(len(frequencias), 3)
        self.assertAlmostEqual(frequencias[0], 261.63, delta=0.01)  # Do
        self.assertAlmostEqual(frequencias[1], 329.63, delta=0.01)  # Mi
        self.assertAlmostEqual(frequencias[2], 392.00, delta=0.01)  # Sol

    def test_nota_para_indice(self):
        """Testa a conversão de nota para índice."""
        self.assertEqual(nota_para_indice("do"), 0)
        self.assertEqual(nota_para_indice("la"), 9)
        self.assertEqual(nota_para_indice("do", "#"), 1)
        self.assertEqual(nota_para_indice("re", "b"), 1)

    def test_indice_para_frequencia(self):
        """Testa a conversão de índice para frequência."""
        # Lá (A4) tem o índice MIDI 69 e frequência 440Hz
        self.assertAlmostEqual(indice_para_frequencia(69), 440.0)
        self.assertAlmostEqual(indice_para_frequencia(60), 261.63, delta=0.01)  # Dó (C4)


if __name__ == "__main__":
    unittest.main()
