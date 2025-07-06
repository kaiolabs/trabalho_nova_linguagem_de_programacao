"""
Processador de comandos de estruturas da linguagem MelodyScript.
Inclui condicionais, repetições, blocos paralelos, etc.
"""

import re


class ComandosEstruturas:
    """Processador de comandos de estruturas (condicionais, repetições, blocos paralelos, etc)."""

    def __init__(self, processador):
        """
        Inicializa o processador de comandos de estruturas.

        Args:
            processador: Processador principal que orquestra todos os comandos
        """
        self.processador = processador

    @property
    def parser(self):
        """Acessa o parser principal através do processador."""
        return self.processador.parser

    def processar_blocos_paralelos(self, conteudo, comandos, pos_inicial):
        """
        Processa blocos paralelos no conteúdo.

        Args:
            conteudo: String com o conteúdo a ser processado
            comandos: Lista onde os comandos serão adicionados
            pos_inicial: Posição inicial a considerar no conteúdo

        Returns:
            Nova posição após processar blocos paralelos
        """
        # Padrão para blocos paralelos
        padrao_bloco_paralelo = r"inicio_paralelo\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\s*fim_paralelo"

        for match in re.finditer(padrao_bloco_paralelo, conteudo):
            # Processar os comandos antes do bloco paralelo
            self.processador.processar_comandos_simples(conteudo[pos_inicial : match.start()], comandos)

            # Bloco de execução paralela
            bloco_paralelo = match.group(1).strip()

            # Adicionar comando de início paralelo
            comandos.append({"tipo": "inicio_paralelo"})

            # Processar comandos dentro do bloco paralelo
            bloco_comandos = []
            self.processador.processar_comandos_melodia(bloco_paralelo, bloco_comandos)
            comandos.extend(bloco_comandos)

            # Adicionar comando de fim paralelo
            comandos.append({"tipo": "fim_paralelo"})

            pos_inicial = match.end()

        return pos_inicial

    def processar_condicionais(self, conteudo, comandos, pos_inicial):
        """
        Processa estruturas condicionais no conteúdo.

        Args:
            conteudo: String com o conteúdo a ser processado
            comandos: Lista onde os comandos serão adicionados
            pos_inicial: Posição inicial a considerar no conteúdo

        Returns:
            Nova posição após processar condicionais
        """
        # Padrão para condicionais
        padrao_condicional = r"se\s*\(\s*([^)]+)\s*\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}(?:\s*senao\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\})?"

        for match in re.finditer(padrao_condicional, conteudo[pos_inicial:]):
            # Ajustar índices para a posição correta
            match_start = match.start() + pos_inicial
            match_end = match.end() + pos_inicial

            # Processar os comandos antes da condicional
            self.processador.processar_comandos_simples(conteudo[pos_inicial:match_start], comandos)

            # Processar a condição
            condicao = match.group(1).strip()
            bloco_verdadeiro = match.group(2).strip()
            bloco_falso = match.group(3).strip() if match.group(3) else None

            # Adicionar comando condicional
            comandos.append(
                {
                    "tipo": "condicional",
                    "condicao": condicao,
                    "bloco_verdadeiro": [],
                    "bloco_falso": [] if bloco_falso else None,
                }
            )

            # Processar blocos da condicional
            self.processador.processar_comandos_melodia(bloco_verdadeiro, comandos[-1]["bloco_verdadeiro"])
            if bloco_falso:
                self.processador.processar_comandos_melodia(bloco_falso, comandos[-1]["bloco_falso"])

            pos_inicial = match_end

        return pos_inicial

    def processar_para_cada(self, conteudo, comandos, pos_inicial):
        """
        Processa estruturas de iteração "para cada" no conteúdo.

        Args:
            conteudo: String com o conteúdo a ser processado
            comandos: Lista onde os comandos serão adicionados
            pos_inicial: Posição inicial a considerar no conteúdo

        Returns:
            Nova posição após processar iterações
        """
        # Padrão para para_cada
        padrao_para_cada = r"para\s+cada\s+(\w+)\s+em\s+(\w+|reverso\(\w+\))\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"

        for match in re.finditer(padrao_para_cada, conteudo[pos_inicial:]):
            # Ajustar índices para a posição correta
            match_start = match.start() + pos_inicial
            match_end = match.end() + pos_inicial

            # Processar os comandos antes da iteração
            self.processador.processar_comandos_simples(conteudo[pos_inicial:match_start], comandos)

            # Processar a iteração
            variavel_iteracao = match.group(1).strip()
            colecao = match.group(2).strip()
            bloco_iteracao = match.group(3).strip()

            # Verificar se é uma coleção com reverso
            reverso = False
            if colecao.startswith("reverso(") and colecao.endswith(")"):
                reverso = True
                colecao = colecao[8:-1].strip()  # Extrair o nome da coleção

            # Adicionar comando para_cada
            comandos.append(
                {
                    "tipo": "para_cada",
                    "variavel": variavel_iteracao,
                    "colecao": colecao,
                    "reverso": reverso,
                    "comandos": [],
                }
            )

            # Processar comandos do bloco de iteração
            self.processador.processar_comandos_melodia(bloco_iteracao, comandos[-1]["comandos"])

            pos_inicial = match_end

        return pos_inicial

    def processar_repeticoes(self, conteudo, comandos, pos_inicial):
        """
        Processa estruturas de repetição no conteúdo.

        Args:
            conteudo: String com o conteúdo a ser processado
            comandos: Lista onde os comandos serão adicionados
            pos_inicial: Posição inicial a considerar no conteúdo

        Returns:
            Nova posição após processar repetições
        """
        # Padrão para repetições
        padrao_repeticao = r"repetir\s+(\d+)\s+vezes\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"

        for match in re.finditer(padrao_repeticao, conteudo[pos_inicial:]):
            # Ajustar índices para a posição correta
            match_start = match.start() + pos_inicial
            match_end = match.end() + pos_inicial

            # Processar os comandos antes da repetição
            self.processador.processar_comandos_simples(conteudo[pos_inicial:match_start], comandos)

            # Processar a repetição
            vezes = int(match.group(1))
            conteudo_repeticao = match.group(2)

            comandos_repeticao = []
            self.processador.processar_comandos_melodia(conteudo_repeticao, comandos_repeticao)

            # Adicionar os comandos repetidos
            comandos.append({"tipo": "repeticao", "vezes": vezes, "comandos": comandos_repeticao})

            pos_inicial = match_end

        return pos_inicial
