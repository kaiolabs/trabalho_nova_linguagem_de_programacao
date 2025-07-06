"""
Verificador semântico para MelodyScript.
Responsável por verificar a semântica do código e detectar problemas lógicos.
"""

import re
from typing import List

from .utils import obter_erros_comuns, remover_comentarios


class SemanticChecker:
    """Verificador semântico para código MelodyScript."""

    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o verificador semântico.

        Args:
            debug_mode: Se deve ativar o modo de debug
        """
        self.debug_mode = debug_mode
        self.avisos = []

    def verificar_semantica(self, conteudo: str) -> List[str]:
        """
        Verifica a semântica do código MelodyScript.

        Args:
            conteudo: Conteúdo do arquivo MelodyScript

        Returns:
            Lista de avisos encontrados
        """
        self.avisos = []

        # Remover comentários para análise semântica
        conteudo_sem_comentarios = remover_comentarios(conteudo)

        # Verificar erros comuns de digitação
        self._verificar_erros_digitacao(conteudo_sem_comentarios)

        return self.avisos

    def _verificar_erros_digitacao(self, conteudo: str) -> None:
        """
        Verifica erros comuns de digitação no código.

        Args:
            conteudo: Conteúdo sem comentários
        """
        erros_comuns = obter_erros_comuns()

        # Verificar palavras escritas incorretamente
        for palavra_errada, correcao in erros_comuns.items():
            if re.search(r"\b" + palavra_errada + r"\b", conteudo, re.IGNORECASE):
                self.avisos.append(f"Possível erro de digitação: '{palavra_errada}'. Você quis dizer '{correcao}'?")
