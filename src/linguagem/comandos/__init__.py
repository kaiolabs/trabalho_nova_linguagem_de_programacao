"""
Pacote de comandos da linguagem MelodyScript.
Este pacote contém os módulos para processamento de diferentes tipos de comandos.
"""

from src.linguagem.comandos.comandos_estruturas import ComandosEstruturas
from src.linguagem.comandos.comandos_simples import ComandosSimples
from src.linguagem.comandos.processador import ProcessadorComandos

__all__ = ["ProcessadorComandos", "ComandosSimples", "ComandosEstruturas"]
