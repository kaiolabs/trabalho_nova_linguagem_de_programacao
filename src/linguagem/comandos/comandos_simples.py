"""
Processador de comandos simples da linguagem MelodyScript.
Inclui tocar notas, pausas, configurações, etc.
"""

import re


class ComandosSimples:
    """Processador de comandos simples (notas, pausas, configurações, etc)."""

    def __init__(self, processador):
        """
        Inicializa o processador de comandos simples.

        Args:
            processador: Processador principal que orquestra todos os comandos
        """
        self.processador = processador

    @property
    def parser(self):
        """Acessa o parser principal através do processador."""
        return self.processador.parser

    def processar(self, conteudo, comandos):
        """
        Processa comandos simples (tocar, pausa, configurações).

        Esta versão preserva a ordem sequencial dos comandos.

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
            self._processar_comando_tocar_acorde_literal(match, comandos)
            return

        # 2. Tocar acorde definido ou nota sem modificador
        match = re.match(r"tocar\s+(\w+)(?!\s+([#b]))(?!\w)\s+(\w+)", linha)
        if match:
            self._processar_comando_tocar_nota_ou_acorde(match, comandos)
            return

        # 3. Tocar nota com modificador após espaço
        match = re.match(r"tocar\s+(\w+)\s+([#b])\s+(\w+)", linha)
        if match:
            self._processar_comando_tocar_nota_com_modificador(match, comandos)
            return

        # 4. Tocar nota com modificador junto
        match = re.match(r"tocar\s+(\w+)([#b])\s+(\w+)", linha)
        if match:
            self._processar_comando_tocar_nota_com_modificador(match, comandos)
            return

        # 5. Tocar nota com número de oitava
        match = re.match(r"tocar\s+(\w+\d+)\s+(\w+)", linha)
        if match:
            self._processar_comando_tocar_nota_com_oitava(match, comandos)
            return

        # 6. Tocar nota com modificador e número de oitava (separados)
        match = re.match(r"tocar\s+(\w+)\s+([#b])\s*(\d+)\s+(\w+)", linha)
        if match:
            self._processar_comando_tocar_nota_modificador_oitava(match, comandos)
            return

        # 7. Tocar nota com modificador e número de oitava (juntos)
        match = re.match(r"tocar\s+(\w+)([#b])(\d+)\s+(\w+)", linha)
        if match:
            self._processar_comando_tocar_nota_modificador_oitava(match, comandos)
            return

        # Comando pausa
        match = re.match(r"pausa\s+(\w+)", linha)
        if match:
            self._processar_comando_pausa(match, comandos)
            return

        # Comando configurar_envelope (com parâmetros em linha)
        match = re.match(
            r"configurar_envelope\s+attack=([0-9.]+)\s+decay=([0-9.]+)\s+sustain=([0-9.]+)\s+release=([0-9.]+)", linha
        )
        if match:
            self._processar_comando_configurar_envelope(match, comandos)
            return

        # Comando configurar_envelope (dentro de uma melodia)
        match = re.match(
            r"configurar_envelope\s*\{\s*attack\s*=\s*([\d\.]+)\s*;\s*decay\s*=\s*([\d\.]+)\s*;\s*sustain\s*=\s*([\d\.]+)\s*;\s*release\s*=\s*([\d\.]+)\s*;\s*\}",
            linha,
        )
        if match:
            self._processar_comando_configurar_envelope(match, comandos)
            return

        # Comando configurar_forma_onda
        match = re.match(r"configurar_forma_onda\s+(\w+)", linha)
        if match:
            self._processar_comando_configurar_forma_onda(match, comandos)
            return

        # Comando instrumento
        match = re.match(r"instrumento\s+(\w+)", linha)
        if match:
            self._processar_comando_instrumento(match, comandos)
            return

        # Chamadas de função
        match = re.match(r"(\w+)\s*\(\s*([^)]*)\s*\)", linha)
        if match:
            self._processar_comando_funcao(match, comandos)
            return

        # Se chegou aqui e a linha não está vazia, pode ser um comando não reconhecido
        if linha.strip():
            print(f"Aviso: Linha não reconhecida como comando: '{linha}'")

    def _processar_comando_tocar_acorde_literal(self, match, comandos):
        """Processa comando tocar para acordes literais com sintaxe <nota1 nota2 ...>"""
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

    def _processar_comando_tocar_nota_ou_acorde(self, match, comandos):
        """Processa comando tocar para acordes definidos ou notas sem modificador"""
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

    def _processar_comando_tocar_nota_com_modificador(self, match, comandos):
        """Processa comando tocar para notas com modificador"""
        nota = match.group(1)
        modificador = match.group(2)
        duracao = match.group(3)

        comandos.append({"tipo": "tocar", "nota": nota, "modificador": modificador, "duracao": duracao})

    def _processar_comando_tocar_nota_com_oitava(self, match, comandos):
        """Processa comando tocar para notas com número de oitava"""
        nota = match.group(1)  # Por exemplo: "do4"
        duracao = match.group(2)

        comandos.append({"tipo": "tocar", "nota": nota, "modificador": None, "duracao": duracao})

    def _processar_comando_tocar_nota_modificador_oitava(self, match, comandos):
        """Processa comando tocar para notas com modificador e número de oitava"""
        if len(match.groups()) == 4:  # Caso: nota+espaço+modificador+oitava
            nota_base = match.group(1)  # Nota base (ex: "do")
            modificador = match.group(2)  # Modificador (ex: "#")
            oitava = match.group(3)  # Número da oitava (ex: "4")
            duracao = match.group(4)
        else:  # Caso: nota+modificador+oitava (juntos)
            nota_base = match.group(1)  # Nota base (ex: "do")
            modificador = match.group(2)  # Modificador (ex: "#")
            oitava = match.group(3)  # Número da oitava (ex: "4")
            duracao = match.group(4)

        # Combina nota base e oitava em uma única nota (ex: "do4")
        nota = f"{nota_base}{oitava}"

        comandos.append({"tipo": "tocar", "nota": nota, "modificador": modificador, "duracao": duracao})

    def _processar_comando_pausa(self, match, comandos):
        """Processa comando pausa"""
        duracao = match.group(1)
        comandos.append({"tipo": "pausa", "duracao": duracao})

    def _processar_comando_configurar_envelope(self, match, comandos):
        """Processa comando para configuração de envelope ADSR"""
        comandos.append(
            {
                "tipo": "configurar_envelope",
                "attack": float(match.group(1)),
                "decay": float(match.group(2)),
                "sustain": float(match.group(3)),
                "release": float(match.group(4)),
            }
        )

    def _processar_comando_configurar_forma_onda(self, match, comandos):
        """Processa comando para configuração de forma de onda"""
        waveform = match.group(1)
        comandos.append({"tipo": "configurar_forma_onda", "waveform": waveform})

    def _processar_comando_instrumento(self, match, comandos):
        """Processa comando para configuração de instrumento"""
        nome_instrumento = match.group(1)
        comandos.append({"tipo": "instrumento", "nome": nome_instrumento})

    def _processar_comando_funcao(self, match, comandos):
        """Processa chamadas de função"""
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
            return True

        return False
