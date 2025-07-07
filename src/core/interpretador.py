"""
Interpretador para a linguagem MelodyScript.
Coordena a execução de programas MelodyScript.
"""

import copy
import sys

from src.audio.sintetizador import AudioEngine
from src.linguagem.parser import MelodyScriptParser
from src.utils.teoria_musical import calcular_duracao, calcular_frequencia


class MelodyScriptInterpretador:
    """Interpretador para a linguagem MelodyScript."""

    def __init__(self):
        """Inicializa o interpretador."""
        self.parser = MelodyScriptParser()
        self.audio_engine = AudioEngine()
        self.variaveis = {}
        self.escopo_atual = {}  # Para armazenar variáveis de escopo local durante execução de funções
        self._debug_mode = False  # Modo de debug, padrão desligado

    def carregar_arquivo(self, caminho):
        """
        Carrega e parseia um arquivo MelodyScript.

        Args:
            caminho: Caminho para o arquivo a ser carregado

        Returns:
            True se o carregamento foi bem-sucedido, False caso contrário
        """
        # Configurar o modo de debug no parser
        if hasattr(self.parser, "debug_mode"):
            self.parser.debug_mode = self._debug_mode

        resultado = self.parser.parsear_arquivo(caminho)

        # Exibir informações de debug se o modo estiver ativado
        if self._debug_mode and resultado:
            print("DEBUG: Informações do arquivo carregado:")
            print(f"  - Tempo: {self.parser.tempo} BPM")
            print(f"  - Instrumento: {self.parser.instrumento}")
            print(f"  - Forma de onda: {self.parser.waveform}")
            print(f"  - Melodias: {len(self.parser.melodias)}")
            print(f"  - Acordes definidos: {len(self.parser.acordes)}")
            print(f"  - Funções definidas: {len(self.parser.funcoes)}")

        return resultado

    def executar_melodia(self, nome_melodia=None):
        """
        Executa uma melodia carregada.

        Args:
            nome_melodia: Nome da melodia a ser executada. Se None, usa a primeira melodia encontrada.

        Returns:
            True se a execução foi bem-sucedida, False caso contrário
        """
        if not nome_melodia and self.parser.melodias:
            # Se não for especificado, usar a primeira melodia
            nome_melodia = list(self.parser.melodias.keys())[0]

        if nome_melodia not in self.parser.melodias:
            print(f"Erro: Melodia '{nome_melodia}' não encontrada.")
            return False

        print(f"Executando melodia: {nome_melodia}")

        # Aplicar configurações globais (envelope ADSR, forma de onda)
        self._aplicar_configuracoes_globais()

        # Executar os comandos da melodia
        self._executar_comandos(self.parser.melodias[nome_melodia])

        # Se estiver no modo paralelo, aguardar todos os sons terminarem antes de finalizar
        if hasattr(self.parser, "modo_paralelo") and self.parser.modo_paralelo:
            print("Aguardando todos os sons terminarem...")
            self.audio_engine.aguardar_todos_sons()

        print(f"Melodia '{nome_melodia}' concluída!")
        return True

    def _executar_comandos(self, comandos):
        """
        Executa uma lista de comandos.

        Args:
            comandos: Lista de comandos a executar
        """
        modo_paralelo_ativo = False  # Rastrear se estamos dentro de um bloco paralelo

        for comando in comandos:
            tipo = comando["tipo"]

            if self._debug_mode:
                print(f"DEBUG: Executando comando tipo '{tipo}'")

            # Comandos de controle do modo paralelo
            if tipo == "inicio_paralelo":
                if self._debug_mode:
                    print("DEBUG: Iniciando bloco paralelo")
                self.audio_engine.salvar_estado_paralelo()
                self.audio_engine.habilitar_modo_paralelo(True)
                modo_paralelo_ativo = True
                continue  # Pular para o próximo comando

            elif tipo == "fim_paralelo":
                if self._debug_mode:
                    print("DEBUG: Finalizando bloco paralelo")
                # Se estamos no fim de um bloco paralelo, esperar todos os sons terminarem
                if modo_paralelo_ativo:
                    print("Aguardando sons do bloco paralelo terminarem...")
                    self.audio_engine.aguardar_todos_sons()
                self.audio_engine.restaurar_estado_paralelo()
                modo_paralelo_ativo = False
                continue  # Pular para o próximo comando

            # Comandos regulares
            if tipo == "tocar":
                self._executar_comando_tocar(comando)
            elif tipo == "tocar_acorde":
                self._executar_comando_tocar_acorde(comando)
            elif tipo == "pausa":
                self._executar_comando_pausa(comando)
            elif tipo == "configurar_envelope":
                self._executar_comando_configurar_envelope(comando)
            elif tipo == "configurar_forma_onda":
                self._executar_comando_configurar_forma_onda(comando)
            elif tipo == "condicional":
                self._executar_comando_condicional(comando)
            elif tipo == "repeticao":
                self._executar_comando_repeticao(comando)
            elif tipo == "chamada_funcao":
                self._executar_comando_funcao(comando)
            elif tipo == "para_cada":
                self._executar_comando_para_cada(comando)
            elif tipo == "instrumento":
                self._executar_comando_instrumento(comando)
            else:
                print(f"Aviso: Comando tipo '{tipo}' não reconhecido. Ignorando.")

        # Se ainda estamos em modo paralelo ao final dos comandos, aguardar todos os sons
        if modo_paralelo_ativo:
            print("Aguardando sons do bloco paralelo terminarem...")
            self.audio_engine.aguardar_todos_sons()
            self.audio_engine.restaurar_estado_paralelo()

    def _executar_comando_tocar(self, comando):
        """
        Executa um comando para tocar uma nota.

        Args:
            comando: Comando a executar
        """
        nota = comando["nota"]
        modificador = comando["modificador"]
        duracao_nome = comando["duracao"]

        try:
            # Calcular a frequência da nota
            frequencia = calcular_frequencia(nota, modificador)

            # Calcular a duração real em segundos
            duracao_segundos = calcular_duracao(duracao_nome, self.parser.tempo)

            # Tocar a nota
            instrumento_atual = self.audio_engine.instrumento_atual
            print(
                f"Tocando {nota}{modificador if modificador else ''} ({duracao_nome}) - Instrumento: {instrumento_atual}"
            )
            sys.stdout.flush()  # Garantir exibição imediata
            self.audio_engine.tocar_nota(frequencia, duracao_segundos)

        except ValueError as e:
            # Parar execução imediatamente em caso de nota ou duração inválida
            print(f"\033[91m❌ {str(e)}\033[0m")
            print("\033[91m🛑 Execução interrompida devido a erro na nota/duração.\033[0m")
            raise SystemExit(1)

    def _executar_comando_tocar_acorde(self, comando):
        """
        Executa um comando para tocar um acorde.

        Args:
            comando: Comando a executar
        """
        duracao_nome = comando["duracao"]
        notas = comando["notas"]
        nome_acorde = comando.get("nome_acorde")

        try:
            # Verificar se o nome_acorde é uma variável e resolvê-la se necessário
            if nome_acorde:
                if nome_acorde in self.escopo_atual:
                    # Se o acorde estiver no escopo local, usar ele diretamente
                    if isinstance(self.escopo_atual[nome_acorde], list):
                        notas = self.escopo_atual[nome_acorde]
                elif nome_acorde in self.variaveis:
                    # Se o acorde estiver no escopo global, usar ele diretamente
                    if isinstance(self.variaveis[nome_acorde], list):
                        notas = self.variaveis[nome_acorde]

            # Calcular a duração real em segundos
            duracao_segundos = calcular_duracao(duracao_nome, self.parser.tempo)

            # Calcular as frequências de todas as notas do acorde
            frequencias = []
            notas_str = []

            for nota_info in notas:
                nota = nota_info["nota"]
                modificador = nota_info["modificador"]
                frequencia = calcular_frequencia(nota, modificador)
                frequencias.append(frequencia)
                notas_str.append(f"{nota}{modificador if modificador else ''}")

            # Informação sobre acorde tocado
            if nome_acorde:
                print(
                    f"Tocando acorde {nome_acorde} ({', '.join(notas_str)}) ({duracao_nome}) - Instrumento: {self.audio_engine.instrumento_atual}"
                )
            else:
                print(
                    f"Tocando acorde <{' '.join(notas_str)}> ({duracao_nome}) - Instrumento: {self.audio_engine.instrumento_atual}"
                )
            sys.stdout.flush()  # Garantir exibição imediata

            # Tocar o acorde
            self.audio_engine.tocar_nota(frequencias, duracao_segundos)

        except ValueError as e:
            # Parar execução imediatamente em caso de nota ou duração inválida
            print(f"\033[91m❌ {str(e)}\033[0m")
            print("\033[91m🛑 Execução interrompida devido a erro no acorde.\033[0m")
            raise SystemExit(1)

    def _executar_comando_pausa(self, comando):
        """
        Executa um comando de pausa.

        Args:
            comando: Comando a executar
        """
        duracao_nome = comando["duracao"]

        try:
            # Calcular a duração real em segundos
            duracao_segundos = calcular_duracao(duracao_nome, self.parser.tempo)

            # Fazer uma pausa
            instrumento_atual = self.audio_engine.instrumento_atual
            print(f"Pausa ({duracao_nome}) - Instrumento: {instrumento_atual}")

            # Garantir que a mensagem seja exibida imediatamente
            sys.stdout.flush()

            # Executar a pausa
            self.audio_engine.pausa(duracao_segundos)

        except ValueError as e:
            # Parar execução imediatamente em caso de duração inválida
            print(f"\033[91m❌ {str(e)}\033[0m")
            print("\033[91m🛑 Execução interrompida devido a erro na duração da pausa.\033[0m")
            raise SystemExit(1)

    def _executar_comando_configurar_envelope(self, comando):
        """
        Executa um comando para configurar o envelope ADSR.

        Args:
            comando: Comando a executar
        """
        # Aplicar configurações de envelope ADSR
        self.audio_engine.configurar_envelope(
            attack=comando.get("attack"),
            decay=comando.get("decay"),
            sustain=comando.get("sustain"),
            release=comando.get("release"),
        )
        print(
            f"Envelope ADSR configurado: A={self.audio_engine.attack}, D={self.audio_engine.decay}, S={self.audio_engine.sustain}, R={self.audio_engine.release} - Instrumento: {self.audio_engine.instrumento_atual}"
        )
        sys.stdout.flush()  # Garantir exibição imediata

    def _executar_comando_configurar_forma_onda(self, comando):
        """
        Executa um comando para configurar a forma de onda.

        Args:
            comando: Comando a executar
        """
        # Configurar forma de onda
        self.audio_engine.configurar_forma_onda(comando["waveform"])
        print(
            f"Forma de onda configurada: {self.audio_engine.waveform} - Instrumento: {self.audio_engine.instrumento_atual}"
        )
        sys.stdout.flush()  # Garantir exibição imediata

    def _executar_comando_condicional(self, comando):
        """
        Executa um comando condicional (se-senao).

        Args:
            comando: Comando a executar
        """
        condicao = comando["condicao"]
        bloco_verdadeiro = comando["bloco_verdadeiro"]
        bloco_falso = comando["bloco_falso"]

        # Avaliar a condição
        resultado = self._avaliar_condicao(condicao)

        if resultado:
            print(f"Condição '{condicao}' verdadeira, executando bloco principal")
            self._executar_comandos(bloco_verdadeiro)
        elif bloco_falso:
            print(f"Condição '{condicao}' falsa, executando bloco alternativo")
            self._executar_comandos(bloco_falso)
        else:
            print(f"Condição '{condicao}' falsa, pulando bloco")

    def _executar_comando_repeticao(self, comando):
        """
        Executa um comando de repetição.

        Args:
            comando: Comando a executar
        """
        vezes = comando["vezes"]
        comandos_repetir = comando["comandos"]

        print(f"Repetindo bloco {vezes} vezes")

        for i in range(vezes):
            print(f"Repetição {i + 1}/{vezes}")
            self._executar_comandos(comandos_repetir)

    def _executar_comando_funcao(self, comando):
        """
        Executa uma chamada de função.

        Args:
            comando: Comando a executar
        """
        nome_funcao = comando["nome_funcao"]
        argumentos = comando["argumentos"]

        # Verificar se a função existe
        if nome_funcao in self.parser.funcoes:
            funcao = self.parser.funcoes[nome_funcao]

            if "acao" in funcao:
                # Função predefinida com implementação em lambda
                try:
                    # Passar o contexto (self) para resolver variáveis
                    resultado = funcao["acao"](argumentos, self)
                    print(f"Função '{nome_funcao}' executada: {resultado}")
                    return resultado
                except Exception as e:
                    print(f"Erro ao executar função predefinida '{nome_funcao}': {str(e)}")
                    return None
            else:
                # Função definida pelo usuário
                print(f"Executando função '{nome_funcao}'")

                # Criar um novo escopo para as variáveis locais
                escopo_anterior = self.escopo_atual.copy()
                self.escopo_atual = {}

                # Associar argumentos aos parâmetros
                parametros = funcao["parametros"]

                # Validar número de argumentos
                if len(argumentos) != len(parametros):
                    print(
                        f"Erro: Função '{nome_funcao}' espera {len(parametros)} argumentos, mas recebeu {len(argumentos)}"
                    )
                    self.escopo_atual = escopo_anterior  # Restaurar escopo anterior
                    return None

                # Associar valores dos argumentos aos parâmetros
                for i, parametro in enumerate(parametros):
                    nome_param = parametro["nome"]
                    # Verificar se é um acorde definido
                    if argumentos[i] in self.parser.acordes:
                        self.escopo_atual[nome_param] = self.parser.acordes[argumentos[i]]
                    else:
                        # Verificar se é uma variável
                        if argumentos[i] in self.variaveis:
                            self.escopo_atual[nome_param] = self.variaveis[argumentos[i]]
                        elif argumentos[i] == "tempo":
                            self.escopo_atual[nome_param] = self.parser.tempo
                        else:
                            # Valor literal
                            self.escopo_atual[nome_param] = argumentos[i]

                # Executar o corpo da função
                comandos_funcao = []
                self.parser.processador_comandos.processar_comandos_melodia(funcao["corpo"], comandos_funcao)

                # Pré-processar os comandos para substituir referências a variáveis pelos seus valores
                comandos_funcao_processados = self._processar_comandos_com_variaveis(comandos_funcao)

                # Executar os comandos processados
                resultado = self._executar_comandos(comandos_funcao_processados)

                # Restaurar o escopo anterior
                self.escopo_atual = escopo_anterior

                return resultado
        else:
            print(f"Erro: Função '{nome_funcao}' não encontrada.")
            return None

    def _executar_comando_para_cada(self, comando):
        """
        Executa um comando de iteração "para cada".

        Args:
            comando: Comando a executar
        """
        variavel = comando["variavel"]
        colecao_nome = comando["colecao"]
        reverso = comando["reverso"]
        comandos_iteracao = comando["comandos"]

        # Resolver a coleção a ser iterada
        colecao = None

        # Verificar em todos os possíveis locais de definição da coleção
        if colecao_nome in self.escopo_atual:
            # Verificar no escopo atual
            colecao = self.escopo_atual[colecao_nome]
            print(f"Usando coleção '{colecao_nome}' do escopo atual")
        elif colecao_nome in self.parser.acordes:
            # Verificar nos acordes definidos
            colecao = self.parser.acordes[colecao_nome]
            print(f"Usando acorde '{colecao_nome}' definido globalmente")
        elif colecao_nome in self.variaveis:
            # Verificar nas variáveis globais
            colecao = self.variaveis[colecao_nome]
            print(f"Usando coleção '{colecao_nome}' do escopo global")
        else:
            # Se não encontrou a coleção, reportar erro
            print(f"Erro: Coleção '{colecao_nome}' não encontrada para iteração.")
            return

        # Verificar se a coleção é uma lista ou similar
        if not isinstance(colecao, list) and not (
            isinstance(colecao, str) and colecao.startswith("<") and colecao.endswith(">")
        ):
            print(f"Erro: '{colecao_nome}' não é uma coleção válida para iteração.")
            return

        # Extrair notas de uma string literal de acorde se necessário
        if isinstance(colecao, str) and colecao.startswith("<") and colecao.endswith(">"):
            colecao_str = colecao[1:-1].strip()
            colecao = []
            for nota_str in colecao_str.split():
                # Processar nota literal
                nota = nota_str
                modificador = None

                if "#" in nota_str:
                    nota = nota_str[:-1]
                    modificador = "#"
                elif "b" in nota_str:
                    nota = nota_str[:-1]
                    modificador = "b"

                colecao.append({"nota": nota, "modificador": modificador})

        # Aplicar reverso se necessário
        if reverso:
            if isinstance(colecao, list):
                colecao = colecao[::-1]
                print(f"Aplicando reversão à coleção '{colecao_nome}'")
            else:
                print(f"Aviso: Não é possível reverter '{colecao_nome}', que não é uma lista.")
                return

        # Informar sobre a iteração
        print(f"Iterando sobre {colecao_nome} {'(reverso)' if reverso else ''} com {len(colecao)} elementos")

        # Executar comandos para cada elemento
        escopo_anterior = self.escopo_atual.copy()

        for elemento in colecao:
            # Definir a variável de iteração no escopo atual
            self.escopo_atual[variavel] = elemento

            # Log para depuração
            if isinstance(elemento, dict) and "nota" in elemento:
                nota = elemento["nota"]
                mod = elemento["modificador"] if elemento["modificador"] else ""
                print(f"  Iterando elemento: {nota}{mod}")
            else:
                print(f"  Iterando elemento: {elemento}")

            # Pré-processar os comandos para substituir referências a variáveis pelos seus valores
            comandos_processados = self._processar_comandos_com_variaveis(comandos_iteracao)

            # Executar os comandos processados
            self._executar_comandos(comandos_processados)

        # Restaurar o escopo anterior
        self.escopo_atual = escopo_anterior

    def _processar_comandos_com_variaveis(self, comandos):
        """
        Processa os comandos substituindo referências a variáveis pelos seus valores.

        Args:
            comandos: Lista de comandos a processar

        Returns:
            Lista de comandos com variáveis substituídas
        """
        comandos_processados = []

        for comando in comandos:
            # Fazer uma cópia profunda do comando para não alterar o original
            comando_processado = copy.deepcopy(comando)

            # Processar de acordo com o tipo de comando
            if comando["tipo"] == "tocar":
                # Se a nota for uma variável, substitui pelo seu valor
                nota = comando["nota"]
                if nota in self.escopo_atual:
                    # Se for uma nota de um acorde, tem campos "nota" e "modificador"
                    if isinstance(self.escopo_atual[nota], dict) and "nota" in self.escopo_atual[nota]:
                        comando_processado["nota"] = self.escopo_atual[nota]["nota"]
                        comando_processado["modificador"] = self.escopo_atual[nota]["modificador"]
                    else:
                        comando_processado["nota"] = str(self.escopo_atual[nota])
                elif nota in self.variaveis:
                    # Se estiver nas variáveis globais
                    if isinstance(self.variaveis[nota], dict) and "nota" in self.variaveis[nota]:
                        comando_processado["nota"] = self.variaveis[nota]["nota"]
                        comando_processado["modificador"] = self.variaveis[nota]["modificador"]
                    else:
                        comando_processado["nota"] = str(self.variaveis[nota])

                # Garantir que a nota tenha um valor válido depois da substituição
                if not isinstance(comando_processado["nota"], str) or not comando_processado["nota"]:
                    print(f"Aviso: Nota '{nota}' não reconhecida ou não definida.")
                    comando_processado["nota"] = "do"  # Valor padrão para evitar erros

                # Se a duração for uma variável, substitui pelo seu valor
                duracao = comando["duracao"]
                if duracao in self.escopo_atual:
                    comando_processado["duracao"] = str(self.escopo_atual[duracao])
                elif duracao in self.variaveis:
                    comando_processado["duracao"] = str(self.variaveis[duracao])

                # Garantir que a duração tenha um valor válido depois da substituição
                if not isinstance(comando_processado["duracao"], str) or not comando_processado["duracao"]:
                    print(f"Aviso: Duração '{duracao}' não reconhecida ou não definida.")
                    comando_processado["duracao"] = "seminima"  # Valor padrão para evitar erros

            elif comando["tipo"] == "tocar_acorde":
                # Se o acorde for uma variável, substitui pelo seu valor
                if "nome_acorde" in comando:
                    nome_acorde = comando["nome_acorde"]
                    if nome_acorde in self.escopo_atual:
                        if isinstance(self.escopo_atual[nome_acorde], list):
                            comando_processado["notas"] = self.escopo_atual[nome_acorde]
                    elif nome_acorde in self.variaveis:
                        if isinstance(self.variaveis[nome_acorde], list):
                            comando_processado["notas"] = self.variaveis[nome_acorde]
                    elif nome_acorde in self.parser.acordes:
                        comando_processado["notas"] = self.parser.acordes[nome_acorde]

                # Se a duração for uma variável, substitui pelo seu valor
                duracao = comando["duracao"]
                if duracao in self.escopo_atual:
                    comando_processado["duracao"] = str(self.escopo_atual[duracao])
                elif duracao in self.variaveis:
                    comando_processado["duracao"] = str(self.variaveis[duracao])

                # Garantir que a duração tenha um valor válido depois da substituição
                if not isinstance(comando_processado["duracao"], str) or not comando_processado["duracao"]:
                    print(f"Aviso: Duração '{duracao}' não reconhecida ou não definida.")
                    comando_processado["duracao"] = "seminima"  # Valor padrão para evitar erros

            elif comando["tipo"] == "condicional":
                # Processar os blocos de comandos recursivamente
                comando_processado["bloco_verdadeiro"] = self._processar_comandos_com_variaveis(
                    comando["bloco_verdadeiro"]
                )
                if comando["bloco_falso"] is not None:
                    comando_processado["bloco_falso"] = self._processar_comandos_com_variaveis(comando["bloco_falso"])

            elif comando["tipo"] == "repeticao":
                # Se o número de vezes for uma variável, substitui pelo seu valor
                if isinstance(comando["vezes"], str):
                    vezes_str = comando["vezes"]
                    if vezes_str in self.escopo_atual:
                        comando_processado["vezes"] = int(self.escopo_atual[vezes_str])
                    elif vezes_str in self.variaveis:
                        comando_processado["vezes"] = int(self.variaveis[vezes_str])

                # Processar os comandos recursivamente
                comando_processado["comandos"] = self._processar_comandos_com_variaveis(comando["comandos"])

            elif comando["tipo"] == "para_cada":
                # Processar os comandos recursivamente
                comando_processado["comandos"] = self._processar_comandos_com_variaveis(comando["comandos"])

                # Se a coleção for uma variável ou acorde, substitui pelo seu valor na execução
                colecao = comando["colecao"]
                comando_processado["colecao"] = colecao  # Mantém o nome, pois será resolvido em tempo de execução

            elif comando["tipo"] == "chamada_funcao":
                # Processar argumentos da função
                for i, arg in enumerate(comando_processado["argumentos"]):
                    # Se o argumento for uma variável, substitui pelo seu valor
                    if arg in self.escopo_atual:
                        comando_processado["argumentos"][i] = str(self.escopo_atual[arg])
                    elif arg in self.variaveis:
                        comando_processado["argumentos"][i] = str(self.variaveis[arg])

            comandos_processados.append(comando_processado)

        return comandos_processados

    def _avaliar_condicao(self, condicao):
        """
        Avalia uma condição para estruturas condicionais.

        Args:
            condicao: String com a condição a ser avaliada

        Returns:
            Resultado booleano da avaliação
        """
        # Implementação básica para demonstração
        # Suporta apenas condições simples como "var == valor"
        if "==" in condicao:
            esquerda, direita = condicao.split("==")
            esquerda = esquerda.strip()
            direita = direita.strip()

            # Resolver valor da esquerda
            if esquerda in self.escopo_atual:
                valor_esquerda = self.escopo_atual[esquerda]
            elif esquerda in self.variaveis:
                valor_esquerda = self.variaveis[esquerda]
            else:
                try:
                    valor_esquerda = float(esquerda)
                except ValueError:
                    # Remover aspas para strings literais
                    if esquerda.startswith('"') and esquerda.endswith('"'):
                        valor_esquerda = esquerda[1:-1]
                    else:
                        valor_esquerda = esquerda

            # Resolver valor da direita
            if direita in self.escopo_atual:
                valor_direita = self.escopo_atual[direita]
            elif direita in self.variaveis:
                valor_direita = self.variaveis[direita]
            else:
                try:
                    valor_direita = float(direita)
                except ValueError:
                    # Remover aspas para strings literais
                    if direita.startswith('"') and direita.endswith('"'):
                        valor_direita = direita[1:-1]
                    else:
                        valor_direita = direita

            # Comparar valores
            return valor_esquerda == valor_direita
        elif "!=" in condicao:
            esquerda, direita = condicao.split("!=")
            esquerda = esquerda.strip()
            direita = direita.strip()

            # Mesmo processo de resolução que acima
            # Resolver valor da esquerda
            if esquerda in self.escopo_atual:
                valor_esquerda = self.escopo_atual[esquerda]
            elif esquerda in self.variaveis:
                valor_esquerda = self.variaveis[esquerda]
            else:
                try:
                    valor_esquerda = float(esquerda)
                except ValueError:
                    # Remover aspas para strings literais
                    if esquerda.startswith('"') and esquerda.endswith('"'):
                        valor_esquerda = esquerda[1:-1]
                    else:
                        valor_esquerda = esquerda

            # Resolver valor da direita
            if direita in self.escopo_atual:
                valor_direita = self.escopo_atual[direita]
            elif direita in self.variaveis:
                valor_direita = self.variaveis[direita]
            else:
                try:
                    valor_direita = float(direita)
                except ValueError:
                    # Remover aspas para strings literais
                    if direita.startswith('"') and direita.endswith('"'):
                        valor_direita = direita[1:-1]
                    else:
                        valor_direita = direita

            # Comparar valores (desigualdade)
            return valor_esquerda != valor_direita
        else:
            # Outros operadores não implementados
            print(f"Aviso: Condição complexa '{condicao}' não suportada. Tratando como falso.")
            return False

    def _aplicar_configuracoes_globais(self):
        """Aplica configurações globais ao motor de áudio."""
        # Aplicar instrumento se definido
        if hasattr(self.parser, "instrumento") and self.parser.instrumento:
            self.audio_engine.configurar_instrumento(self.parser.instrumento)
            if self._debug_mode:
                print(f"DEBUG: Configurando instrumento: {self.parser.instrumento}")

        # Aplicar envelope ADSR se definido
        if self.parser.envelope:
            self.audio_engine.configurar_envelope(
                attack=self.parser.envelope.get("attack"),
                decay=self.parser.envelope.get("decay"),
                sustain=self.parser.envelope.get("sustain"),
                release=self.parser.envelope.get("release"),
            )

        # Aplicar forma de onda se definida
        if self.parser.waveform:
            self.audio_engine.configurar_forma_onda(self.parser.waveform)

        # Configurar modo paralelo se definido
        if hasattr(self.parser, "modo_paralelo"):
            self.audio_engine.habilitar_modo_paralelo(self.parser.modo_paralelo)
            if self._debug_mode:
                print(f"DEBUG: Configurando modo paralelo: {'Ativado' if self.parser.modo_paralelo else 'Desativado'}")

    def _executar_comando_iniciar_paralelo(self):
        """
        Executa um comando para iniciar a reprodução paralela temporária.
        """
        print("Iniciando bloco de reprodução paralela")
        self.audio_engine.ativar_paralelo_temporario()

    def _executar_comando_parar_paralelo(self):
        """
        Executa um comando para parar a reprodução paralela temporária.
        """
        print("Finalizando bloco de reprodução paralela")
        self.audio_engine.desativar_paralelo_temporario()

    @property
    def tempo(self):
        """Getter para o tempo (BPM)."""
        return self.parser.tempo

    @property
    def instrumento(self):
        """Getter para o instrumento."""
        return self.parser.instrumento

    @property
    def melodias(self):
        """Getter para as melodias."""
        return self.parser.melodias

    @property
    def debug_mode(self):
        """Getter para o modo de debug."""
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        """Setter para o modo de debug."""
        self._debug_mode = bool(value)

    def _executar_comando_instrumento(self, comando):
        """
        Executa um comando para configurar o instrumento atual.

        Args:
            comando: Comando a executar contendo o nome do instrumento
        """
        nome_instrumento = comando["nome"]

        # Configura o instrumento no motor de áudio
        if self.audio_engine.configurar_instrumento(nome_instrumento):
            print(f"Instrumento alterado para: {nome_instrumento}")
            sys.stdout.flush()  # Garantir exibição imediata
        else:
            print(f"Erro ao configurar instrumento: {nome_instrumento}")
            sys.stdout.flush()  # Garantir exibição imediata
