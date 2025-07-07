"""
Processador de definições da linguagem MelodyScript.
Responsável por processar as definições globais, acordes, funções e melodias.
"""

import re


class ProcessadorDefinicoes:
    """Processador de definições da linguagem MelodyScript."""

    def __init__(self, parser):
        """
        Inicializa o processador de definições.

        Args:
            parser: Instância do parser principal
        """
        self.parser = parser

    def processar_definicoes_globais(self, conteudo):
        """
        Processa as definições globais do arquivo (tempo, instrumento, envelope, forma de onda).

        Args:
            conteudo: String com o conteúdo limpo do arquivo
        """
        # Processar definição de tempo
        match_tempo = re.search(r"tempo\s*=\s*(\d+)", conteudo)
        # Processar definição de tempo alternativa
        if not match_tempo:
            match_tempo = re.search(r"tempo\s+(\d+)", conteudo)

        if match_tempo:
            self.parser.tempo = int(match_tempo.group(1))
            print(f"Tempo definido: {self.parser.tempo} BPM")

        # Processar definição de instrumento (global)
        match_instrumento = re.search(r"^instrumento\s+(\w+)", conteudo)
        if match_instrumento:
            self.parser.instrumento = match_instrumento.group(1)
            print(f"Instrumento definido: {self.parser.instrumento}")

        # Processar definição de envelope ADSR
        match_envelope = re.search(
            r"envelope\s*\{\s*attack\s*=\s*([\d\.]+)\s*;\s*decay\s*=\s*([\d\.]+)\s*;\s*sustain\s*=\s*([\d\.]+)\s*;\s*release\s*=\s*([\d\.]+)\s*;\s*\}",
            conteudo,
        )
        if match_envelope:
            self.parser.envelope = {
                "attack": float(match_envelope.group(1)),
                "decay": float(match_envelope.group(2)),
                "sustain": float(match_envelope.group(3)),
                "release": float(match_envelope.group(4)),
            }
            print(
                f"Envelope ADSR definido: A={self.parser.envelope['attack']}, D={self.parser.envelope['decay']}, S={self.parser.envelope['sustain']}, R={self.parser.envelope['release']}"
            )

        # Processar definição de forma de onda
        match_waveform = re.search(r"forma_onda\s+(\w+)", conteudo)
        if match_waveform:
            self.parser.waveform = match_waveform.group(1)
            print(f"Forma de onda definida: {self.parser.waveform}")

    def processar_definicoes_acordes(self, conteudo):
        """
        Processa as definições de acordes no arquivo.

        Args:
            conteudo: String com o conteúdo limpo do arquivo
        """
        padrao_acorde = r"acorde\s+(\w+)\s*=\s*<([^>]+)>"
        for match in re.finditer(padrao_acorde, conteudo):
            nome_acorde = match.group(1)
            notas_str = match.group(2).strip()

            # Separar as notas do acorde
            notas = []
            for nota_str in notas_str.split():
                # Verificar se a nota tem modificador
                if "#" in nota_str:
                    nota = nota_str[:-1]
                    modificador = "#"
                elif "b" in nota_str:
                    nota = nota_str[:-1]
                    modificador = "b"
                else:
                    nota = nota_str
                    modificador = None

                notas.append({"nota": nota, "modificador": modificador})

            self.parser.acordes[nome_acorde] = notas
            print(f"Acorde '{nome_acorde}' definido com {len(notas)} notas")

    def processar_definicoes_funcoes(self, conteudo):
        """
        Processa as definições de funções definidas pelo usuário no arquivo.

        Args:
            conteudo: String com o conteúdo limpo do arquivo
        """
        padrao_funcao = r"funcao\s+(\w+)\s*\(([^)]*)\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"
        for match in re.finditer(padrao_funcao, conteudo):
            nome_funcao = match.group(1)
            params_str = match.group(2).strip()
            corpo_funcao = match.group(3)

            # Processar parâmetros da função
            parametros = []
            if params_str:
                for param in params_str.split(","):
                    param = param.strip()
                    if param:
                        parametros.append({"nome": param})

            # Adicionar a função ao dicionário de funções
            self.parser.funcoes[nome_funcao] = {
                "parametros": parametros,
                "corpo": corpo_funcao,
            }
            print(f"Função '{nome_funcao}' definida com {len(parametros)} parâmetros")

    def encontrar_fechamento_bloco(self, conteudo, pos_inicial):
        """
        Encontra a posição de fechamento de um bloco que começa com chave.

        Args:
            conteudo: String com o conteúdo
            pos_inicial: Posição inicial (da chave de abertura)

        Returns:
            Posição da chave de fechamento correspondente ou -1 se não encontrar
        """
        nivel = 1
        pos = pos_inicial + 1

        while pos < len(conteudo) and nivel > 0:
            if conteudo[pos] == "{":
                nivel += 1
            elif conteudo[pos] == "}":
                nivel -= 1
            pos += 1

        return pos - 1 if nivel == 0 else -1

    def extrair_comandos_melodia(self, conteudo_melodia):
        """
        Extrai e formata os comandos da melodia para facilitar o processamento linha a linha.

        Args:
            conteudo_melodia: Conteúdo bruto da melodia

        Returns:
            String formatada com os comandos da melodia, um por linha
        """
        # Remover comentários e dividir por linhas
        linhas = []
        for linha in conteudo_melodia.split("\n"):
            if "//" in linha:
                linha = linha.split("//")[0]
            linha = linha.strip()
            if linha:
                linhas.append(linha)

        # Conteúdo completo para busca preservando espaços
        conteudo_completo = " ".join(linhas)

        # Estrutura para armazenar comandos com suas posições
        comandos_ordenados = []

        # Padrões de comandos a serem extraídos
        padroes = [
            (r"configurar_forma_onda\s+(\w+)", lambda m: f"configurar_forma_onda {m.group(1)}"),
            (
                r"configurar_envelope\s+attack=([0-9.]+)\s+decay=([0-9.]+)\s+sustain=([0-9.]+)\s+release=([0-9.]+)",
                lambda m: f"configurar_envelope attack={m.group(1)} decay={m.group(2)} sustain={m.group(3)} release={m.group(4)}",
            ),
            (r"tocar\s+<([^>]+)>\s+(\w+)", lambda m: f"tocar <{m.group(1)}> {m.group(2)}"),
            (
                r"tocar\s+(\w+)(?:\s+([#b]))?\s+(\w+)",
                lambda m: f"tocar {m.group(1)}{' ' + m.group(2) if m.group(2) else ''} {m.group(3)}",
            ),
            (r"pausa\s+(\w+)", lambda m: f"pausa {m.group(1)}"),
            (r"instrumento\s+(\w+)", lambda m: f"instrumento {m.group(1)}"),
        ]

        # Encontrar todos os comandos e suas posições no texto
        for padrao, formatter in padroes:
            for match in re.finditer(padrao, conteudo_completo):
                comandos_ordenados.append((match.start(), formatter(match)))

        # Ordenar comandos pela posição de início no texto original
        comandos_ordenados.sort(key=lambda x: x[0])

        # Extrair apenas os comandos formatados, já na ordem correta
        comandos = [cmd for _, cmd in comandos_ordenados]

        if self.parser._debug_mode:
            print(f"DEBUG: Encontrados {len(comandos)} comandos na ordem correta:")
            for i, cmd in enumerate(comandos):
                print(f"  {i + 1}. {cmd}")

        return "\n".join(comandos)

    def processar_melodias(self, conteudo):
        """
        Processa as definições de melodias no arquivo.

        Args:
            conteudo: String com o conteúdo limpo do arquivo
        """
        # Usar um método mais robusto para encontrar melodias
        padrao_melodia_inicio = r"melodia\s+(\w+)\s*\{"

        # Encontrar todos os inícios de melodias
        for match in re.finditer(padrao_melodia_inicio, conteudo):
            nome_melodia = match.group(1)
            pos_inicial_bloco = match.end() - 1  # Posição da chave de abertura

            # Encontrar o fechamento correspondente do bloco
            pos_final_bloco = self.encontrar_fechamento_bloco(conteudo, pos_inicial_bloco)

            if pos_final_bloco == -1:
                print(f"ERRO: Não foi possível encontrar o fechamento do bloco da melodia '{nome_melodia}'")
                continue

            # Extrair o conteúdo da melodia (sem as chaves)
            conteudo_melodia = conteudo[pos_inicial_bloco + 1 : pos_final_bloco]

            # DEBUG: Mostrar detalhes da melodia encontrada
            print(f"DEBUG: Melodia encontrada: '{nome_melodia}'")
            print("DEBUG: Conteúdo da melodia bruto:")
            print("-----------------------------------")
            print(conteudo_melodia)
            print("-----------------------------------")

            self.parser.melodias[nome_melodia] = []
            # Usar o processador de comandos completo que suporta estruturas (repetições, condicionais, etc.)
            self.parser.processador_comandos.processar_comandos_melodia(
                conteudo_melodia, self.parser.melodias[nome_melodia]
            )

            print(f"Melodia '{nome_melodia}' carregada com {len(self.parser.melodias[nome_melodia])} comandos")
