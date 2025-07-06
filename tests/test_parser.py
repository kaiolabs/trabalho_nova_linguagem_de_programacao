"""
Testes para o parser da MelodyScript.
"""

import sys
import unittest
from pathlib import Path

# Adicionar o diretório raiz ao path para permitir importações relativas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.linguagem.parser import MelodyScriptParser


class TestParser(unittest.TestCase):
    """Testes para o MelodyScriptParser."""

    def setUp(self):
        """Configura o ambiente para os testes."""
        self.parser = MelodyScriptParser()

    def test_reset(self):
        """Testa o método reset."""
        self.parser.tempo = 140
        self.parser.instrumento = "guitarra"
        self.parser.melodias = {"teste": []}
        self.parser.acordes = {"teste": []}
        self.parser.variaveis = {"teste": "valor"}
        self.parser.envelope = {"attack": 0.1}
        self.parser.waveform = "square"

        self.parser.reset()

        self.assertEqual(self.parser.tempo, 120)
        self.assertEqual(self.parser.instrumento, "piano")
        self.assertEqual(self.parser.melodias, {})
        self.assertEqual(self.parser.acordes, {})
        self.assertEqual(self.parser.variaveis, {})
        self.assertEqual(self.parser.envelope, {})
        self.assertEqual(self.parser.waveform, "")

    def test_processar_conteudo(self):
        """Testa o processamento de conteúdo básico."""
        conteudo = """
        # Este é um comentário
        tempo = 140  # Definição de tempo
        instrumento guitarra
        
        acorde DoMaior = <do mi sol>
        
        melodia simples {
            tocar do minima
            pausa seminima
        }
        """

        self.parser._processar_conteudo(conteudo)

        self.assertEqual(self.parser.tempo, 140)
        self.assertEqual(self.parser.instrumento, "guitarra")
        self.assertIn("DoMaior", self.parser.acordes)
        self.assertIn("simples", self.parser.melodias)
        self.assertEqual(len(self.parser.melodias["simples"]), 2)


if __name__ == "__main__":
    unittest.main()
