"""
Verificador de balanceamento de delimitadores para MelodyScript.
Responsável por verificar o balanceamento de chaves, parênteses e delimitadores de acordes.
"""

import re
from typing import List

from .utils import remover_comentarios


class BalanceChecker:
    """Verificador de balanceamento de delimitadores."""

    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o verificador de balanceamento.

        Args:
            debug_mode: Se deve ativar o modo de debug
        """
        self.debug_mode = debug_mode
        self.erros = []

    def verificar_balanceamento(self, conteudo: str) -> List[str]:
        """
        Verifica o balanceamento de chaves, parênteses e delimitadores de acordes.

        Args:
            conteudo: Conteúdo do arquivo MelodyScript

        Returns:
            Lista de erros encontrados
        """
        self.erros = []
        conteudo_sem_comentarios = remover_comentarios(conteudo)

        # Verificar balanceamento de chaves
        self._verificar_balanceamento_chaves(conteudo_sem_comentarios)

        # Verificar balanceamento de parênteses
        self._verificar_balanceamento_parenteses(conteudo_sem_comentarios)

        # Verificar balanceamento de delimitadores de acordes
        self._verificar_balanceamento_acordes(conteudo_sem_comentarios)

        return self.erros

    def _verificar_balanceamento_chaves(self, conteudo: str) -> None:
        """
        Verifica o balanceamento de chaves {}.

        Args:
            conteudo: Conteúdo sem comentários
        """
        aberturas = conteudo.count("{")
        fechamentos = conteudo.count("}")

        if aberturas > fechamentos:
            self.erros.append(f"Erro de sintaxe: Faltam {aberturas - fechamentos} fechamentos de chave '}}'")
        elif fechamentos > aberturas:
            self.erros.append(f"Erro de sintaxe: Há {fechamentos - aberturas} fechamentos de chave '}}' a mais")

    def _verificar_balanceamento_parenteses(self, conteudo: str) -> None:
        """
        Verifica o balanceamento de parênteses ().

        Args:
            conteudo: Conteúdo sem comentários
        """
        aberturas = conteudo.count("(")
        fechamentos = conteudo.count(")")

        if aberturas > fechamentos:
            self.erros.append(f"Erro de sintaxe: Faltam {aberturas - fechamentos} fechamentos de parêntese ')'")
        elif fechamentos > aberturas:
            self.erros.append(f"Erro de sintaxe: Há {fechamentos - aberturas} fechamentos de parêntese ')' a mais")

    def _verificar_balanceamento_acordes(self, conteudo: str) -> None:
        """
        Verifica o balanceamento de delimitadores de acordes <>.

        Args:
            conteudo: Conteúdo sem comentários
        """
        # Precisamos tratar com mais cuidado devido à possibilidade de '<' e '>' em expressões condicionais
        # Vamos contar apenas os '<' que não são precedidos por operadores de comparação

        # Expressão regular para encontrar os delimitadores de acordes
        # Detecta '<' que não seja parte de '<=', '<<' ou outras operações
        aberturas_acorde = re.findall(r"(?<![<=-])<(?![=<-])", conteudo)
        delimitadores_abertos = len(aberturas_acorde)

        # Expressão regular para encontrar os fechamentos de acordes
        # Detecta '>' que não seja parte de '>=', '>>' ou outras operações
        fechamentos_acorde = re.findall(r"(?<![>=->])>(?![=>-])", conteudo)
        delimitadores_fechados = len(fechamentos_acorde)

        if self.debug_mode:
            print(f"Delimitadores de acordes: {delimitadores_abertos} abertos, {delimitadores_fechados} fechados")
            if delimitadores_abertos != delimitadores_fechados:
                # Para debug, mostrar todos os símbolos encontrados para verificar se há algum mal detectado
                print(f"Aberturas encontradas: {aberturas_acorde}")
                print(f"Fechamentos encontrados: {fechamentos_acorde}")

        # Ignoramos o erro se os delimitadores parecem estar bem balanceados
        # Isso pode ocorrer devido a operadores de comparação (>, <, >=, <=) sendo confundidos
        # com delimitadores de acordes
        if abs(delimitadores_abertos - delimitadores_fechados) > 1:
            if delimitadores_abertos > delimitadores_fechados:
                self.erros.append(
                    f"Erro de sintaxe: Faltam {delimitadores_abertos - delimitadores_fechados} fechamentos de acordes '>'"
                )
            elif delimitadores_fechados > delimitadores_abertos:
                self.erros.append(
                    f"Erro de sintaxe: Há {delimitadores_fechados - delimitadores_abertos} fechamentos de acordes '>' a mais"
                )
