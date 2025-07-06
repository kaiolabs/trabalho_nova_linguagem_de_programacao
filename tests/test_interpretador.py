"""
Testes para o interpretador da MelodyScript.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Adicionar o diretório raiz ao path para permitir importações relativas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.interpretador import MelodyScriptInterpretador


class TestInterpretador(unittest.TestCase):
    """Testes para o MelodyScriptInterpretador."""

    def setUp(self):
        """Configura o ambiente para os testes."""
        # Mock para o motor de áudio
        self.audio_engine_patcher = patch("src.audio.sintetizador.AudioEngine")
        self.mock_audio_engine = self.audio_engine_patcher.start()

        # Criar instância do interpretador
        self.interpretador = MelodyScriptInterpretador()

        # Substituir o motor de áudio real pelo mock
        self.interpretador.audio_engine = MagicMock()

        # Mock para o parser
        self.parser_patcher = patch("src.linguagem.parser.MelodyScriptParser")
        self.mock_parser = self.parser_patcher.start()
        self.interpretador.parser = MagicMock()

    def tearDown(self):
        """Limpa o ambiente após os testes."""
        self.audio_engine_patcher.stop()
        self.parser_patcher.stop()

    def test_executar_comando_tocar(self):
        """Testa a execução do comando tocar."""
        # Configurar parser mock
        self.interpretador.parser.tempo = 120

        # Comando tocar
        comando = {"tipo": "tocar", "nota": "do", "modificador": None, "duracao": "minima"}

        # Executar o comando
        self.interpretador._executar_comando_tocar(comando)

        # Verificar se o método tocar_nota foi chamado corretamente
        self.interpretador.audio_engine.tocar_nota.assert_called_once()

        # Verificar se os parâmetros estão corretos
        args, _ = self.interpretador.audio_engine.tocar_nota.call_args
        self.assertAlmostEqual(args[0], 261.63, delta=0.01)  # Frequência do Dó
        self.assertEqual(args[1], 1.0)  # Duração da mínima a 120 BPM

    def test_executar_comando_pausa(self):
        """Testa a execução do comando pausa."""
        # Configurar parser mock
        self.interpretador.parser.tempo = 120

        # Comando pausa
        comando = {"tipo": "pausa", "duracao": "seminima"}

        # Executar o comando
        self.interpretador._executar_comando_pausa(comando)

        # Verificar se o método pausa foi chamado corretamente
        self.interpretador.audio_engine.pausa.assert_called_once()

        # Verificar se os parâmetros estão corretos
        args, _ = self.interpretador.audio_engine.pausa.call_args
        self.assertEqual(args[0], 0.5)  # Duração da semínima a 120 BPM

    def test_executar_melodia(self):
        """Testa a execução de uma melodia."""
        # Configurar parser mock com uma melodia
        self.interpretador.parser.melodias = {
            "teste": [
                {"tipo": "tocar", "nota": "do", "modificador": None, "duracao": "minima"},
                {"tipo": "pausa", "duracao": "seminima"},
                {"tipo": "tocar", "nota": "re", "modificador": None, "duracao": "minima"},
            ]
        }

        # Executar a melodia
        with patch.object(self.interpretador, "_executar_comandos") as mock_executar:
            self.interpretador.executar_melodia("teste")

            # Verificar se o método _executar_comandos foi chamado com os comandos corretos
            mock_executar.assert_called_once_with(self.interpretador.parser.melodias["teste"])


if __name__ == "__main__":
    unittest.main()
