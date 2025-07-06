"""
Módulo de linguagem do MelodyScript.
Contém componentes relacionados à definição e processamento da linguagem.
"""

from src.linguagem.funcoes_padrao import definir_funcoes_padrao
from src.linguagem.parser import MelodyScriptParser
from src.linguagem.parser_comandos import ProcessadorComandos
from src.linguagem.parser_definicoes import ProcessadorDefinicoes

__all__ = ["MelodyScriptParser", "ProcessadorComandos", "ProcessadorDefinicoes", "definir_funcoes_padrao"]
