"""
Verificador de sintaxe para MelodyScript.
Responsável por analisar a sintaxe do código e identificar erros estruturais.
"""

import re
from typing import List, Set

from .utils import (
    obter_duracoes_validas,
    obter_formas_onda_validas,
    obter_funcoes_sistema,
    remover_comentarios,
    verifica_parametro_funcao,
)


class SyntaxChecker:
    """Verificador de sintaxe para código MelodyScript."""

    def __init__(self, debug_mode: bool = False):
        """
        Inicializa o verificador de sintaxe.

        Args:
            debug_mode: Se deve ativar o modo de debug
        """
        self.debug_mode = debug_mode
        self.erros = []
        self.avisos = []

    def verificar_sintaxe(self, conteudo: str) -> tuple[List[str], List[str]]:
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
        funcoes_definidas = self._encontrar_funcoes_definidas(linhas)

        if self.debug_mode:
            print(f"Funções definidas: {funcoes_definidas}")

        for i, linha in enumerate(linhas):
            num_linha = i + 1
            linha_limpa = remover_comentarios(linha).strip()

            # Ignorar linhas vazias
            if not linha_limpa:
                continue

            self._verificar_linha(linha_limpa, num_linha, funcoes_definidas)

        return self.erros, self.avisos

    def _encontrar_funcoes_definidas(self, linhas: List[str]) -> Set[str]:
        """
        Encontra todas as funções definidas no código.

        Args:
            linhas: Lista de linhas do código

        Returns:
            Conjunto com nomes das funções definidas
        """
        funcoes_definidas = set()
        for linha in linhas:
            linha_limpa = remover_comentarios(linha).strip()
            match_funcao = re.search(r"funcao\s+(\w+)\s*\(", linha_limpa)
            if match_funcao:
                funcoes_definidas.add(match_funcao.group(1))
        return funcoes_definidas

    def _verificar_linha(self, linha_limpa: str, num_linha: int, funcoes_definidas: Set[str]) -> None:
        """
        Verifica uma linha específica do código.

        Args:
            linha_limpa: Linha sem comentários e espaços extras
            num_linha: Número da linha no arquivo
            funcoes_definidas: Conjunto de funções definidas no código
        """
        # Verificar sintaxe de tempo
        if self._deve_verificar_tempo(linha_limpa):
            self._verificar_sintaxe_tempo(linha_limpa, num_linha)

        # Verificar sintaxe de instrumento
        elif "instrumento" in linha_limpa and "=" not in linha_limpa:
            self._verificar_sintaxe_instrumento(linha_limpa, num_linha)

        # Verificar sintaxe de forma de onda
        elif "forma_onda" in linha_limpa and "=" not in linha_limpa:
            self._verificar_sintaxe_forma_onda(linha_limpa, num_linha)

        # Verificar sintaxe de definição de acorde
        elif "acorde" in linha_limpa and "=" in linha_limpa:
            self._verificar_sintaxe_acorde(linha_limpa, num_linha)

        # Verificar sintaxe de melodia (abertura)
        elif "melodia" in linha_limpa and "{" in linha_limpa:
            self._verificar_sintaxe_melodia(linha_limpa, num_linha)

        # Verificar sintaxe de comando tocar
        elif linha_limpa.startswith("tocar "):
            self._verificar_sintaxe_tocar(linha_limpa, num_linha)

        # Verificar chamadas de função
        elif "(" in linha_limpa and ")" in linha_limpa and not linha_limpa.startswith("se"):
            self._verificar_chamadas_funcao(linha_limpa, num_linha, funcoes_definidas)

        # Verificar sintaxe de comando pausa
        elif "pausa" in linha_limpa:
            self._verificar_sintaxe_pausa(linha_limpa, num_linha)

        # Verificar sintaxe de comando repetir
        elif "repetir" in linha_limpa and "vezes" in linha_limpa:
            self._verificar_sintaxe_repetir(linha_limpa, num_linha)

        # Verificar sintaxe de estruturas condicionais
        elif linha_limpa.startswith("se ") and "(" in linha_limpa:
            self._verificar_sintaxe_condicional(linha_limpa, num_linha)

        # Verificar sintaxe de for_each
        elif "para_cada" in linha_limpa:
            self._verificar_sintaxe_para_cada(linha_limpa, num_linha)

    def _deve_verificar_tempo(self, linha_limpa: str) -> bool:
        """
        Verifica se a linha contém uma definição de tempo que deve ser validada.

        Args:
            linha_limpa: Linha limpa para análise

        Returns:
            True se deve verificar, False caso contrário
        """
        return "tempo" in linha_limpa and bool(re.search(r"^\s*tempo\s*=", linha_limpa))

    def _verificar_sintaxe_tempo(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe de definição de tempo."""
        match = re.search(r"tempo\s*=\s*(\d+)\s*;?", linha_limpa)
        if not match:
            self.erros.append(f"Linha {num_linha}: Sintaxe inválida para definição de tempo. Use 'tempo = 120'")

    def _verificar_sintaxe_instrumento(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe de definição de instrumento."""
        match = re.search(r"instrumento\s+(\w+)", linha_limpa)
        if not match:
            self.erros.append(
                f"Linha {num_linha}: Sintaxe inválida para definição de instrumento. Use 'instrumento piano'"
            )
        elif not linha_limpa.endswith(";") and ";" in linha_limpa:
            self.avisos.append(f"Linha {num_linha}: Ponto e vírgula não deve estar no meio da linha")

    def _verificar_sintaxe_forma_onda(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe de definição de forma de onda."""
        match = re.search(r"forma_onda\s+(\w+)", linha_limpa)
        if not match:
            self.erros.append(
                f"Linha {num_linha}: Sintaxe inválida para definição de forma de onda. Use 'forma_onda sine'"
            )
        elif match.group(1) not in obter_formas_onda_validas():
            self.avisos.append(
                f"Linha {num_linha}: Forma de onda '{match.group(1)}' não reconhecida. "
                f"Valores válidos: {', '.join(obter_formas_onda_validas())}"
            )
        elif not linha_limpa.endswith(";") and ";" in linha_limpa:
            self.avisos.append(f"Linha {num_linha}: Ponto e vírgula não deve estar no meio da linha")

    def _verificar_sintaxe_acorde(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe de definição de acorde."""
        match = re.search(r"acorde\s+(\w+)\s*=\s*<([^>]+)>", linha_limpa)
        if not match:
            self.erros.append(
                f"Linha {num_linha}: Sintaxe inválida para definição de acorde. Use 'acorde DoMaior = <do mi sol>'"
            )
        elif not linha_limpa.endswith(";") and ";" in linha_limpa:
            self.avisos.append(f"Linha {num_linha}: Ponto e vírgula não deve estar no meio da linha")

    def _verificar_sintaxe_melodia(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe de definição de melodia."""
        match = re.search(r"melodia\s+(\w+)\s*\{", linha_limpa)
        if not match:
            self.erros.append(
                f"Linha {num_linha}: Sintaxe inválida para início de melodia. Use 'melodia nome_da_melodia {{'"
            )

    def _verificar_sintaxe_tocar(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe do comando tocar."""
        partes = linha_limpa.split()
        if len(partes) < 3:  # 'tocar', nota, duração
            self.erros.append(f"Linha {num_linha}: Sintaxe inválida para comando 'tocar'. Use 'tocar do minima'")
        else:
            nota_ou_acorde = partes[1]
            duracao = partes[2].rstrip(";")

            # Verificar se é uma variável (acorde ou nota)
            if not (
                nota_ou_acorde.startswith("<")
                or verifica_parametro_funcao(nota_ou_acorde)
                or any(nota in nota_ou_acorde.lower() for nota in ["do", "re", "mi", "fa", "sol", "la", "si"])
            ):
                self.avisos.append(f"Linha {num_linha}: Possível erro na nota/acorde '{nota_ou_acorde}'")

            # Verificar se a duração é válida
            duracoes_validas = obter_duracoes_validas()
            if not (duracao in duracoes_validas or verifica_parametro_funcao(duracao)):
                self.erros.append(
                    f"Linha {num_linha}: Duração inválida: '{duracao}'. Valores válidos: {', '.join(duracoes_validas)}"
                )

    def _verificar_chamadas_funcao(self, linha_limpa: str, num_linha: int, funcoes_definidas: Set[str]) -> None:
        """Verifica chamadas de função."""
        match_chamada = re.search(r"(\w+)\s*\(", linha_limpa)
        if match_chamada:
            nome_funcao = match_chamada.group(1)
            funcoes_sistema = obter_funcoes_sistema()
            if nome_funcao not in funcoes_sistema and nome_funcao not in funcoes_definidas:
                if not verifica_parametro_funcao(nome_funcao):
                    self.avisos.append(f"Linha {num_linha}: Possível chamada de função não definida: '{nome_funcao}'")

    def _verificar_sintaxe_pausa(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe do comando pausa."""
        match = re.search(r"pausa\s+(\w+)", linha_limpa)
        if not match:
            self.erros.append(f"Linha {num_linha}: Sintaxe inválida para comando pausa. Use 'pausa minima'")
        elif match.group(1) not in obter_duracoes_validas():
            self.avisos.append(
                f"Linha {num_linha}: Duração '{match.group(1)}' não reconhecida. "
                f"Valores válidos: {', '.join(obter_duracoes_validas())}"
            )

        if not linha_limpa.endswith(";") and ";" in linha_limpa:
            self.avisos.append(f"Linha {num_linha}: Ponto e vírgula não deve estar no meio da linha")

    def _verificar_sintaxe_repetir(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe do comando repetir."""
        match = re.search(r"repetir\s+(\d+)\s+vezes\s*\{", linha_limpa)
        if not match:
            self.erros.append(f"Linha {num_linha}: Sintaxe inválida para comando repetir. Use 'repetir 4 vezes {{'")

    def _verificar_sintaxe_condicional(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe de estruturas condicionais."""
        match = re.search(r"se\s+\(([^)]*)\)\s*\{", linha_limpa)
        if not match:
            self.erros.append(
                f"Linha {num_linha}: Sintaxe inválida para estrutura condicional 'se'. Use 'se (condição) {{'"
            )

    def _verificar_sintaxe_para_cada(self, linha_limpa: str, num_linha: int) -> None:
        """Verifica a sintaxe do comando para_cada."""
        match = re.search(r"para_cada\s+(\w+)\s+em\s+(\w+)\s*\{", linha_limpa)
        if not match and "reverso" not in linha_limpa:
            self.erros.append(
                f"Linha {num_linha}: Sintaxe inválida para 'para_cada'. Use 'para_cada elemento em coleção {{'"
            )
        elif not match and "reverso" in linha_limpa:
            match_reverso = re.search(r"para_cada\s+(\w+)\s+em\s+(\w+)\s+reverso\s*\{", linha_limpa)
            if not match_reverso:
                self.erros.append(
                    f"Linha {num_linha}: Sintaxe inválida para 'para_cada reverso'. "
                    "Use 'para_cada elemento em coleção reverso {'"
                )
