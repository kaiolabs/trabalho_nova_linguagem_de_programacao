"""
Verificador de sintaxe simplificado para MelodyScript.
Versão básica mas funcional para detectar erros principais.
"""

import re
from typing import List, Tuple

from .utils import obter_duracoes_validas, remover_comentarios


class SimpleSyntaxChecker:
    """Verificador de sintaxe simplificado."""

    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o verificador de sintaxe.

        Args:
            debug_mode: Se deve ativar o modo de debug
        """
        self.debug_mode = debug_mode
        self.erros = []
        self.avisos = []

    def verificar_sintaxe(self, conteudo: str) -> Tuple[List[str], List[str]]:
        """
        Verifica a sintaxe do código MelodyScript.

        Args:
            conteudo: Conteúdo do arquivo MelodyScript

        Returns:
            Tupla com (erros, avisos) encontrados
        """
        self.erros = []
        self.avisos = []

        linhas = conteudo.split("\n")

        for i, linha in enumerate(linhas):
            num_linha = i + 1
            linha_limpa = remover_comentarios(linha).strip()

            # Ignorar linhas vazias
            if not linha_limpa:
                continue

            self._verificar_linha_simples(linha_limpa, num_linha)

        return self.erros, self.avisos

    def _verificar_linha_simples(self, linha_limpa: str, num_linha: int) -> None:
        """
        Verifica uma linha específica do código de forma simplificada.

        Args:
            linha_limpa: Linha sem comentários e espaços extras
            num_linha: Número da linha no arquivo
        """
        # Verificar comando tocar
        if linha_limpa.startswith("tocar "):
            self._verificar_comando_tocar(linha_limpa, num_linha)

        # Verificar comando repetir
        elif "repetir" in linha_limpa and "{" in linha_limpa:
            self._verificar_comando_repetir(linha_limpa, num_linha)

    def _verificar_comando_tocar(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe do comando tocar."""
        partes = linha_limpa.split()

        if len(partes) < 3:  # Deve ter: tocar, nota, duração
            self.erros.append(f"Linha {num_linha}: Comando 'tocar' incompleto. Use: 'tocar nota duracao'")
            return

        duracao = partes[2].rstrip(";")
        duracoes_validas = obter_duracoes_validas()

        if duracao not in duracoes_validas:
            self.erros.append(
                f"Linha {num_linha}: Duração '{duracao}' é inválida. "
                f"Use uma das seguintes: {', '.join(duracoes_validas)}"
            )

    def _verificar_comando_repetir(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe do comando repetir."""
        # Deve ter: repetir N vezes {
        match = re.search(r"repetir\s+(\d+)\s+vezes\s*\{", linha_limpa)
        if not match:
            # Verificar se está faltando apenas "vezes"
            match_sem_vezes = re.search(r"repetir\s+(\d+)\s*\{", linha_limpa)
            if match_sem_vezes:
                self.erros.append(f"Linha {num_linha}: Sintaxe incorreta para 'repetir'. Use: 'repetir N vezes {{'")
            else:
                self.erros.append(
                    f"Linha {num_linha}: Sintaxe inválida para comando 'repetir'. Use: 'repetir N vezes {{'"
                )
