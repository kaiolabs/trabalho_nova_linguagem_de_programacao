"""
Processador de comandos da linguagem MelodyScript.
Responsável por processar os comandos de melodias, incluindo repetições, condicionais, etc.
"""

import re


class ProcessadorComandos:
    """Processador de comandos da linguagem MelodyScript."""

    def __init__(self, parser):
        """
        Inicializa o processador de comandos.

        Args:
            parser: Instância do parser principal
        """
        self.parser = parser

    def processar_comandos_melodia(self, conteudo, comandos):
        """
        Processa os comandos dentro de uma melodia.

        Args:
            conteudo: String com o conteúdo da melodia
            comandos: Lista onde os comandos serão adicionados
        """
        # Encontrar blocos paralelos primeiro
        padrao_bloco_paralelo = r"inicio_paralelo\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\s*fim_paralelo"
        pos_inicial = 0

        for match in re.finditer(padrao_bloco_paralelo, conteudo):
            # Processar os comandos antes do bloco paralelo
            self.processar_comandos_simples(conteudo[pos_inicial : match.start()], comandos)

            # Bloco de execução paralela
            bloco_paralelo = match.group(1).strip()

            # Adicionar comando de início paralelo
            comandos.append({"tipo": "inicio_paralelo"})

            # Processar comandos dentro do bloco paralelo
            bloco_comandos = []
            self.processar_comandos_melodia(bloco_paralelo, bloco_comandos)
            comandos.extend(bloco_comandos)

            # Adicionar comando de fim paralelo
            comandos.append({"tipo": "fim_paralelo"})

            pos_inicial = match.end()

        # Encontrar estruturas condicionais
        padrao_condicional = r"se\s*\(\s*([^)]+)\s*\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}(?:\s*senao\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\})?"

        for match in re.finditer(padrao_condicional, conteudo[pos_inicial:]):
            # Ajustar índices para a posição correta
            match_start = match.start() + pos_inicial
            match_end = match.end() + pos_inicial

            # Processar os comandos antes da condicional
            self.processar_comandos_simples(conteudo[pos_inicial:match_start], comandos)

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
            self.processar_comandos_melodia(bloco_verdadeiro, comandos[-1]["bloco_verdadeiro"])
            if bloco_falso:
                self.processar_comandos_melodia(bloco_falso, comandos[-1]["bloco_falso"])

            pos_inicial = match_end

        # Encontrar iterações "para cada"
        padrao_para_cada = r"para\s+cada\s+(\w+)\s+em\s+(\w+|reverso\(\w+\))\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"
        for match in re.finditer(padrao_para_cada, conteudo[pos_inicial:]):
            # Ajustar índices para a posição correta
            match_start = match.start() + pos_inicial
            match_end = match.end() + pos_inicial

            # Processar os comandos antes da iteração
            self.processar_comandos_simples(conteudo[pos_inicial:match_start], comandos)

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
            self.processar_comandos_melodia(bloco_iteracao, comandos[-1]["comandos"])

            pos_inicial = match_end

        # Encontrar repetições
        padrao_repeticao = r"repetir\s+(\d+)\s+vezes\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"

        for match in re.finditer(padrao_repeticao, conteudo[pos_inicial:]):
            # Ajustar índices para a posição correta após processar condicionais
            match_start = match.start() + pos_inicial
            match_end = match.end() + pos_inicial

            # Processar os comandos antes da repetição
            self.processar_comandos_simples(conteudo[pos_inicial:match_start], comandos)

            # Processar a repetição
            vezes = int(match.group(1))
            conteudo_repeticao = match.group(2)

            comandos_repeticao = []
            self.processar_comandos_melodia(conteudo_repeticao, comandos_repeticao)

            # Adicionar os comandos repetidos
            comandos.append({"tipo": "repeticao", "vezes": vezes, "comandos": comandos_repeticao})

            pos_inicial = match_end

        # Processar os comandos após a última estrutura especial
        self.processar_comandos_simples(conteudo[pos_inicial:], comandos)

    def processar_comandos_simples(self, conteudo, comandos):
        """
        Processa comandos simples (tocar, pausa, configurações).

        Esta versão refatorada preserva a ordem sequencial dos comandos.

        Args:
            conteudo: String com o conteúdo a ser processado
            comandos: Lista onde os comandos serão adicionados
        """
        # Padronizar e dividir a entrada por linhas de comando
        linhas = conteudo.replace(";", "\n").split("\n")

        # Processar cada linha na ordem em que aparece
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue  # Pular linhas vazias

            # Processar cada comando de acordo com seu padrão
            self._processar_linha_comando(linha, comandos)

    def _processar_linha_comando(self, linha, comandos):
        """
        Processa uma única linha de comando e adiciona à lista de comandos.

        Args:
            linha: String com a linha a ser processada
            comandos: Lista onde o comando será adicionado
        """
        # Comando de início e fim paralelo
        if re.match(r"inicio_paralelo", linha):
            comandos.append({"tipo": "inicio_paralelo"})
            return

        if re.match(r"fim_paralelo", linha):
            comandos.append({"tipo": "fim_paralelo"})
            return

        # Comandos de tocar nota/acorde
        # 1. Tocar com sintaxe de acorde literal <nota1 nota2 ...>
        match = re.match(r"tocar\s+<([^>]+)>\s+(\w+)", linha)
        if match:
            notas_str = match.group(1).strip()
            duracao = match.group(2)

            notas = []
            for nota_str in notas_str.split():
                # Verificar se a nota tem número de oitava
                digitos_match = re.search(r"(\d+)", nota_str)
                oitava = ""
                if digitos_match:
                    oitava = digitos_match.group(1)
                    nota_str = re.sub(r"\d+", "", nota_str)  # Remove oitava da nota

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

                # Recolocar a oitava na nota
                if oitava:
                    nota = nota + oitava

                notas.append({"nota": nota, "modificador": modificador})

            comandos.append({"tipo": "tocar_acorde", "notas": notas, "duracao": duracao})
            return

        # 2. Tocar acorde definido ou nota sem modificador
        match = re.match(r"tocar\s+(\w+)(?!\s+([#b]))(?!\w)\s+(\w+)", linha)
        if match:
            nome_elemento = match.group(1)
            duracao = match.group(3)

            # Verificar se é um acorde definido
            if nome_elemento in self.parser.acordes:
                frequencias = []
                notas_str = []

                for nota_info in self.parser.acordes[nome_elemento]:
                    nota = nota_info["nota"]
                    modificador = nota_info["modificador"]
                    notas_str.append(f"{nota}{modificador if modificador else ''}")

                comandos.append(
                    {
                        "tipo": "tocar_acorde",
                        "nome_acorde": nome_elemento,
                        "notas": self.parser.acordes[nome_elemento],
                        "duracao": duracao,
                    }
                )
                print(f"Acorde '{nome_elemento}' ({', '.join(notas_str)}) adicionado como comando")
            else:
                # Se não for um acorde, é uma nota normal sem modificador
                comandos.append({"tipo": "tocar", "nota": nome_elemento, "modificador": None, "duracao": duracao})
            return

        # 3. Tocar nota com modificador após espaço
        match = re.match(r"tocar\s+(\w+)\s+([#b])\s+(\w+)", linha)
        if match:
            nota = match.group(1)
            modificador = match.group(2)
            duracao = match.group(3)

            comandos.append({"tipo": "tocar", "nota": nota, "modificador": modificador, "duracao": duracao})
            return

        # 4. Tocar nota com modificador junto
        match = re.match(r"tocar\s+(\w+)([#b])\s+(\w+)", linha)
        if match:
            nota = match.group(1)
            modificador = match.group(2)
            duracao = match.group(3)

            comandos.append({"tipo": "tocar", "nota": nota, "modificador": modificador, "duracao": duracao})
            return

        # 5. Tocar nota com número de oitava
        match = re.match(r"tocar\s+(\w+\d+)\s+(\w+)", linha)
        if match:
            nota = match.group(1)  # Por exemplo: "do4"
            duracao = match.group(2)

            comandos.append({"tipo": "tocar", "nota": nota, "modificador": None, "duracao": duracao})
            return

        # 6. Tocar nota com modificador e número de oitava (separados)
        match = re.match(r"tocar\s+(\w+)\s+([#b])\s*(\d+)\s+(\w+)", linha)
        if match:
            nota_base = match.group(1)  # Nota base (ex: "do")
            modificador = match.group(2)  # Modificador (ex: "#")
            oitava = match.group(3)  # Número da oitava (ex: "4")
            duracao = match.group(4)

            # Combina nota base e oitava em uma única nota (ex: "do4")
            nota = f"{nota_base}{oitava}"

            comandos.append({"tipo": "tocar", "nota": nota, "modificador": modificador, "duracao": duracao})
            return

        # 7. Tocar nota com modificador e número de oitava (juntos)
        match = re.match(r"tocar\s+(\w+)([#b])(\d+)\s+(\w+)", linha)
        if match:
            nota_base = match.group(1)  # Nota base (ex: "do")
            modificador = match.group(2)  # Modificador (ex: "#")
            oitava = match.group(3)  # Número da oitava (ex: "4")
            duracao = match.group(4)

            # Combina nota base e oitava em uma única nota (ex: "do4")
            nota = f"{nota_base}{oitava}"

            comandos.append({"tipo": "tocar", "nota": nota, "modificador": modificador, "duracao": duracao})
            return

        # Comando pausa
        match = re.match(r"pausa\s+(\w+)", linha)
        if match:
            duracao = match.group(1)
            comandos.append({"tipo": "pausa", "duracao": duracao})
            return

        # Comando configurar_envelope (com parâmetros em linha)
        match = re.match(
            r"configurar_envelope\s+attack=([0-9.]+)\s+decay=([0-9.]+)\s+sustain=([0-9.]+)\s+release=([0-9.]+)", linha
        )
        if match:
            comandos.append(
                {
                    "tipo": "configurar_envelope",
                    "attack": float(match.group(1)),
                    "decay": float(match.group(2)),
                    "sustain": float(match.group(3)),
                    "release": float(match.group(4)),
                }
            )
            return

        # Comando configurar_envelope (dentro de uma melodia)
        match = re.match(
            r"configurar_envelope\s*\{\s*attack\s*=\s*([\d\.]+)\s*;\s*decay\s*=\s*([\d\.]+)\s*;\s*sustain\s*=\s*([\d\.]+)\s*;\s*release\s*=\s*([\d\.]+)\s*;\s*\}",
            linha,
        )
        if match:
            comandos.append(
                {
                    "tipo": "configurar_envelope",
                    "attack": float(match.group(1)),
                    "decay": float(match.group(2)),
                    "sustain": float(match.group(3)),
                    "release": float(match.group(4)),
                }
            )
            return

        # Comando configurar_forma_onda
        match = re.match(r"configurar_forma_onda\s+(\w+)", linha)
        if match:
            waveform = match.group(1)
            comandos.append({"tipo": "configurar_forma_onda", "waveform": waveform})
            return

        # Comando instrumento
        match = re.match(r"instrumento\s+(\w+)", linha)
        if match:
            nome_instrumento = match.group(1)
            comandos.append({"tipo": "instrumento", "nome": nome_instrumento})
            return

        # Chamadas de função
        match = re.match(r"(\w+)\s*\(\s*([^)]*)\s*\)", linha)
        if match:
            nome_funcao = match.group(1)
            argumentos_str = match.group(2).strip()

            # Verificar se a função existe
            if nome_funcao in self.parser.funcoes:
                # Processar argumentos
                argumentos = []
                if argumentos_str:
                    for arg in argumentos_str.split(","):
                        argumentos.append(arg.strip())

                comandos.append({"tipo": "chamada_funcao", "nome_funcao": nome_funcao, "argumentos": argumentos})
                print(f"Chamada de função '{nome_funcao}' adicionada como comando")
                return

        # Se chegou aqui e a linha não está vazia, pode ser um comando não reconhecido
        if linha.strip():
            print(f"Aviso: Linha não reconhecida como comando: '{linha}'")
