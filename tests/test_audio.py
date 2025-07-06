"""
Testes para o motor de áudio da MelodyScript.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Adicionar o diretório raiz ao path para permitir importações relativas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.sintetizador import AudioEngine


class TestAudioEngine(unittest.TestCase):
    """Testes para o AudioEngine."""

    def setUp(self):
        """Configura o ambiente para os testes."""
        # Mock para o pygame.mixer
        self.mixer_patcher = patch("pygame.mixer")
        self.mock_mixer = self.mixer_patcher.start()

        # Criar instância do motor de áudio
        self.audio_engine = AudioEngine()

        # Mock para o numpy
        self.numpy_patcher = patch("numpy.sin")
        self.mock_numpy_sin = self.numpy_patcher.start()
        self.mock_numpy_sin.return_value = [0] * 44100  # Array de zeros para simular a onda

    def tearDown(self):
        """Limpa o ambiente após os testes."""
        self.mixer_patcher.stop()
        self.numpy_patcher.stop()

    def test_configurar_envelope(self):
        """Testa a configuração do envelope ADSR."""
        # Valores iniciais
        self.assertEqual(self.audio_engine.attack, 0.02)
        self.assertEqual(self.audio_engine.decay, 0.05)
        self.assertEqual(self.audio_engine.sustain, 0.7)
        self.assertEqual(self.audio_engine.release, 0.05)

        # Configurar novos valores
        self.audio_engine.configurar_envelope(attack=0.1, decay=0.2, sustain=0.5, release=0.3)

        # Verificar se os valores foram atualizados
        self.assertEqual(self.audio_engine.attack, 0.1)
        self.assertEqual(self.audio_engine.decay, 0.2)
        self.assertEqual(self.audio_engine.sustain, 0.5)
        self.assertEqual(self.audio_engine.release, 0.3)

        # Configurar apenas alguns valores
        self.audio_engine.configurar_envelope(attack=0.15, sustain=0.6)

        # Verificar se apenas os valores especificados foram atualizados
        self.assertEqual(self.audio_engine.attack, 0.15)
        self.assertEqual(self.audio_engine.decay, 0.2)  # Não alterado
        self.assertEqual(self.audio_engine.sustain, 0.6)
        self.assertEqual(self.audio_engine.release, 0.3)  # Não alterado

    def test_configurar_forma_onda(self):
        """Testa a configuração da forma de onda."""
        # Valor inicial
        self.assertEqual(self.audio_engine.waveform, "sine")

        # Configurar nova forma de onda válida
        self.audio_engine.configurar_forma_onda("square")
        self.assertEqual(self.audio_engine.waveform, "square")

        # Configurar forma de onda inválida
        with patch("builtins.print") as mock_print:
            self.audio_engine.configurar_forma_onda("invalid")
            self.assertEqual(self.audio_engine.waveform, "sine")  # Deve retornar ao padrão
            mock_print.assert_called_once()  # Deve mostrar um aviso

    @patch("time.sleep")
    def test_pausa(self, mock_sleep):
        """Testa o método de pausa."""
        # Testar pausa
        self.audio_engine.pausa(1.5)

        # Verificar se o sleep foi chamado com a duração correta
        mock_sleep.assert_called_once_with(1.5)


if __name__ == "__main__":
    unittest.main()
