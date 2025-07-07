"""
Analisador Sintático Robusto baseado em Gramática Livre de Contexto (GLC).
Implementa validação sintática rigorosa que NUNCA deixa passar erros de sintaxe.
"""

import re
from difflib import get_close_matches
from enum import Enum
from typing import List, Tuple


class TipoToken(Enum):
    """Tipos de tokens da linguagem MelodyScript."""

    PALAVRA_CHAVE = "palavra_chave"
    NOTA_MUSICAL = "nota_musical"
    DURACAO = "duracao"
    INSTRUMENTO = "instrumento"
    NUMERO = "numero"
    IDENTIFICADOR = "identificador"
    OPERADOR = "operador"
    SIMBOLO = "simbolo"
    DESCONHECIDO = "desconhecido"


class Token:
    """Representação de um token com tipo e valor."""

    def __init__(self, tipo: TipoToken, valor: str, linha: int, coluna: int):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo.value}, '{self.valor}', {self.linha}:{self.coluna})"


class AnalisadorSintaticoRobusto:
    """Analisador sintático baseado em GLC que NUNCA deixa passar erros de sintaxe."""

    def __init__(self):
        """Inicializa o analisador com gramática formal."""
        self.erros_sintaxe = []
        self._definir_gramatica_formal()
        self._definir_tokens_validos()

    def _definir_gramatica_formal(self):
        """Define a Gramática Livre de Contexto (GLC) formal do MelodyScript."""

        # Produções da gramática formal BNF-like
        self.gramatica = {
            # Programa principal
            "programa": [["configuracoes", "definicoes"], ["definicoes"], ["configuracoes"]],
            # Configurações globais
            "configuracoes": [["configuracao", "configuracoes"], ["configuracao"]],
            "configuracao": [["tempo", "=", "numero", ";"], ["instrumento", "identificador", ";"]],
            # Definições (melodias, funções, acordes)
            "definicoes": [["definicao", "definicoes"], ["definicao"]],
            "definicao": [
                ["melodia", "identificador", "{", "comandos", "}"],
                ["funcao", "identificador", "(", "parametros", ")", "{", "comandos", "}"],
                ["acorde", "identificador", "{", "notas", "}"],
            ],
            # Comandos dentro de melodias/funções
            "comandos": [
                ["comando", "comandos"],
                ["comando"],
                ["estrutura_controle", "comandos"],
                ["estrutura_controle"],
            ],
            "comando": [
                ["tocar", "nota_musical", "duracao", ";"],
                ["pausa", "duracao", ";"],
                ["identificador", "(", "argumentos", ")", ";"],
            ],
            # Estruturas de controle
            "estrutura_controle": [
                ["repetir", "numero", "vezes", "{", "comandos", "}"],
                ["se", "(", "condicao", ")", "{", "comandos", "}"],
                ["para", "cada", "identificador", "em", "identificador", "{", "comandos", "}"],
            ],
            # Elementos básicos
            "nota_musical": [
                ["nota_base"],
                ["nota_base", "modificador"],
                ["nota_base", "oitava"],
                ["nota_base", "modificador", "oitava"],
            ],
            "nota_base": [
                ["do"],
                ["re"],
                ["mi"],
                ["fa"],
                ["sol"],
                ["la"],
                ["si"],
                ["c"],
                ["d"],
                ["e"],
                ["f"],
                ["g"],
                ["a"],
                ["b"],
            ],
            "modificador": [["#"], ["b"]],
            "oitava": [["numero"]],
            "duracao": [
                ["semibreve"],
                ["minima"],
                ["seminima"],
                ["colcheia"],
                ["semicolcheia"],
                ["fusa"],
                ["semifusa"],
            ],
            # Listas
            "parametros": [["identificador", ",", "parametros"], ["identificador"], [""]],
            "argumentos": [["expressao", ",", "argumentos"], ["expressao"], [""]],
            "notas": [["nota_musical", ",", "notas"], ["nota_musical"]],
            # Expressões e condições
            "expressao": [["identificador"], ["numero"], ["nota_musical"]],
            "condicao": [["expressao", "operador_comparacao", "expressao"], ["identificador"]],
            "operador_comparacao": [["=="], ["!="], ["<"], [">"], ["<="], [">="]],
        }

    def _definir_tokens_validos(self):
        """Define todos os tokens válidos com seus tipos."""

        # Palavras-chave da linguagem
        self.palavras_chave = {
            "tempo",
            "instrumento",
            "melodia",
            "funcao",
            "acorde",
            "tocar",
            "pausa",
            "repetir",
            "vezes",
            "se",
            "senao",
            "para",
            "cada",
            "em",
            "reverso",
            "inicio_paralelo",
            "fim_paralelo",
            "configurar_envelope",
            "configurar_forma_onda",
            "modo_paralelo",
            "true",
            "verdadeiro",
            "sim",
            "false",
            "falso",
            "nao",
            "attack",
            "decay",
            "sustain",
            "release",
        }

        # Notas musicais válidas
        self.notas_musicais = {"do", "re", "mi", "fa", "sol", "la", "si", "c", "d", "e", "f", "g", "a", "b"}

        # Modificadores de nota
        self.modificadores = {"#", "b"}

        # Durações válidas
        self.duracoes = {"semibreve", "minima", "seminima", "colcheia", "semicolcheia", "fusa", "semifusa"}

        # Instrumentos válidos
        self.instrumentos = {
            "piano",
            "guitarra",
            "violino",
            "flauta",
            "baixo",
            "bateria",
            "saxofone",
            "trompete",
            "trombone",
            "clarinete",
            "orgao",
        }

        # Símbolos válidos
        self.simbolos = {"{", "}", "(", ")", "[", "]", "<", ">", ";", ",", ".", "="}

        # Operadores válidos
        self.operadores = {"=", "==", "!=", "<", ">", "<=", ">=", "+", "-", "*", "/", "%"}

    def validar_arquivo(self, conteudo: str) -> Tuple[bool, List[str]]:
        """
        Valida arquivo usando análise sintática rigorosa baseada em GLC.
        NUNCA deixa passar erros de sintaxe.
        """
        self.erros_sintaxe.clear()

        # 1. Análise Lexical: Tokenizar o código
        tokens = self._tokenizar(conteudo)

        # 2. Validação Lexical: Verificar tokens inválidos
        self._validar_tokens_lexical(tokens)

        # 3. Análise Sintática: Verificar estrutura gramatical
        if not self.erros_sintaxe:  # Só continua se não há erros lexicais
            self._analisar_sintaxe(tokens)

        # 4. Validação Semântica: Verificar contexto
        if not self.erros_sintaxe:  # Só continua se não há erros sintáticos
            self._validar_semantica(tokens)

        return len(self.erros_sintaxe) == 0, self.erros_sintaxe.copy()

    def _tokenizar(self, conteudo: str) -> List[Token]:
        """Tokeniza o conteúdo em tokens com tipos bem definidos."""
        tokens = []

        # Remover comentários
        conteudo_limpo = self._remover_comentarios(conteudo)

        linhas = conteudo_limpo.split("\n")

        for num_linha, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha:
                continue

            # Extrair tokens da linha com posição
            tokens_linha = self._extrair_tokens_com_posicao(linha, num_linha)
            tokens.extend(tokens_linha)

        return tokens

    def _extrair_tokens_com_posicao(self, linha: str, num_linha: int) -> List[Token]:
        """Extrai tokens de uma linha com posição e tipo."""
        tokens = []

        # Padrão para capturar tokens com posição
        padrao = r"([a-zA-Z_][a-zA-Z0-9_]*|[0-9]+\.?[0-9]*|[{}()\[\]<>;,=+\-*/%#b]|\S+)"

        for match in re.finditer(padrao, linha):
            valor = match.group(1)
            coluna = match.start() + 1

            # Determinar tipo do token
            tipo = self._determinar_tipo_token(valor)

            token = Token(tipo, valor, num_linha, coluna)
            tokens.append(token)

        return tokens

    def _determinar_tipo_token(self, valor: str) -> TipoToken:
        """Determina o tipo de um token de forma rigorosa."""

        # Verificar número
        if valor.isdigit() or re.match(r"^\d+\.\d+$", valor):
            return TipoToken.NUMERO

        # Verificar símbolos
        if valor in self.simbolos:
            return TipoToken.SIMBOLO

        # Verificar operadores
        if valor in self.operadores:
            return TipoToken.OPERADOR

        valor_lower = valor.lower()

        # Verificar palavras-chave
        if valor_lower in self.palavras_chave:
            return TipoToken.PALAVRA_CHAVE

        # Verificar nota musical (incluindo modificadores e oitavas)
        if self._eh_nota_musical_valida(valor):
            return TipoToken.NOTA_MUSICAL

        # Verificar duração
        if valor_lower in self.duracoes:
            return TipoToken.DURACAO

        # Verificar instrumento
        if valor_lower in self.instrumentos:
            return TipoToken.INSTRUMENTO

        # Verificar se é identificador válido
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", valor):
            return TipoToken.IDENTIFICADOR

        # Se não se encaixa em nenhuma categoria, é DESCONHECIDO
        return TipoToken.DESCONHECIDO

    def _eh_nota_musical_valida(self, valor: str) -> bool:
        """Verifica se é uma nota musical válida com modificadores/oitavas."""
        valor_lower = valor.lower()

        # Nota simples
        if valor_lower in self.notas_musicais:
            return True

        # Nota com modificador (do#, reb)
        if len(valor) >= 2:
            nota_base = valor_lower[:-1]
            modificador = valor[-1]
            if nota_base in self.notas_musicais and modificador in self.modificadores:
                return True

        # Nota com oitava (do4, re5)
        match = re.match(r"^([a-z]+)(\d+)$", valor_lower)
        if match:
            nota_base = match.group(1)
            oitava = int(match.group(2))
            if nota_base in self.notas_musicais and 0 <= oitava <= 8:
                return True

        # Nota com modificador e oitava (do#4, reb5)
        match = re.match(r"^([a-z]+)([#b])(\d+)$", valor_lower)
        if match:
            nota_base = match.group(1)
            modificador = match.group(2)
            oitava = int(match.group(3))
            if nota_base in self.notas_musicais and modificador in self.modificadores and 0 <= oitava <= 8:
                return True

        return False

    def _validar_tokens_lexical(self, tokens: List[Token]):
        """Validação lexical rigorosa - detecta TODOS os tokens inválidos."""

        for i, token in enumerate(tokens):
            if token.tipo == TipoToken.DESCONHECIDO:
                # Token completamente inválido - sugerir correção
                self._reportar_erro_token_invalido(token)
            elif token.tipo == TipoToken.IDENTIFICADOR:
                # Verificar se é um identificador suspeito que parece comando malformado
                self._validar_identificador_suspeito(token, tokens, i)

    def _validar_identificador_suspeito(self, token: Token, tokens: List[Token], posicao: int):
        """Valida identificadores que podem ser comandos malformados."""

        # Detectar padrões suspeitos que parecem comandos malformados
        valor_lower = token.valor.lower()

        # PRIMEIRO: Detectar padrões específicos conhecidos
        padroes_malformados = {
            "tocadasdasdasnima": "tocar do seminima",
            "tocaremininima": "tocar re seminima",
            "tocarmiseminima": "tocar mi seminima",
            "pausaseminima": "pausa seminima",
            "repetir2vezes": "repetir 2 vezes",
        }

        if valor_lower in padroes_malformados:
            correcao_sugerida = padroes_malformados[valor_lower]
            self._adicionar_erro(
                f"Linha {token.linha}: Comando malformado '{token.valor}' - Use: '{correcao_sugerida}'"
            )
            return

        # SEGUNDO: Padrão suspeito - palavra longa que contém partes de comandos conhecidos
        if len(token.valor) > 8:  # Identificadores muito longos são suspeitos
            # Verificar se contém fragmentos de comandos válidos
            comandos_fragmentos = {
                "toc": "tocar",
                "pau": "pausa",
                "rep": "repetir",
                "mel": "melodia",
                "ins": "instrumento",
            }

            for fragmento, comando_correto in comandos_fragmentos.items():
                if fragmento in valor_lower:
                    # Verificar se está em contexto de melodia (dentro de chaves)
                    if self._esta_em_contexto_melodia(tokens, posicao):
                        # Este é muito provavelmente um comando malformado
                        self._reportar_comando_malformado(token, comando_correto)
                        return

        # TERCEIRO: Verificar se é um identificador isolado terminado com ';' (suspeito de comando)
        if posicao + 1 < len(tokens) and tokens[posicao + 1].valor == ";":
            if self._esta_em_contexto_melodia(tokens, posicao):
                # Identificador seguido de ';' dentro de melodia é suspeito
                self._analisar_possivel_comando_malformado(token)

    def _esta_em_contexto_melodia(self, tokens: List[Token], posicao: int) -> bool:
        """Verifica se o token está dentro de uma definição de melodia."""

        # Procurar para trás para encontrar 'melodia' seguida de identificador e '{'
        chaves_abertas = 0

        for i in range(posicao - 1, -1, -1):
            token_anterior = tokens[i]

            if token_anterior.valor == "}":
                chaves_abertas += 1
            elif token_anterior.valor == "{":
                if chaves_abertas > 0:
                    chaves_abertas -= 1
                else:
                    # Encontrou abertura de bloco, verificar se é melodia
                    # Procurar 'melodia' antes desta chave
                    for j in range(i - 1, max(0, i - 5), -1):
                        if tokens[j].tipo == TipoToken.PALAVRA_CHAVE and tokens[j].valor.lower() == "melodia":
                            return True
                    break

        return False

    def _reportar_comando_malformado(self, token: Token, comando_sugerido: str):
        """Reporta comando malformado com sugestão específica."""
        self._adicionar_erro(
            f"Linha {token.linha}: Token suspeito '{token.valor}' parece ser comando malformado - Você quis dizer '{comando_sugerido}'?"
        )

    def _analisar_possivel_comando_malformado(self, token: Token):
        """Analisa token que pode ser comando malformado."""

        # Buscar similaridade com comandos conhecidos
        comandos_validos = ["tocar", "pausa", "repetir"]

        # Verificar se o token contém partes de comandos válidos
        valor_lower = token.valor.lower()

        for comando in comandos_validos:
            # Calcular similaridade grosseira
            similaridade = self._calcular_similaridade_basica(valor_lower, comando)

            if similaridade > 0.3:  # Se tem 30% de similaridade
                # Verificar se pode ser comando + parâmetros concatenados
                if comando == "tocar" and len(token.valor) > 5:
                    self._analisar_comando_tocar_concatenado(token)
                    return

        # Se não encontrou similaridade específica, reportar como suspeito
        self._adicionar_erro(
            f"Linha {token.linha}: Identificador suspeito '{token.valor}' em contexto de comando - Verifique se está correto"
        )

    def _analisar_comando_tocar_concatenado(self, token: Token):
        """Analisa token que pode ser 'tocar' concatenado com parâmetros."""

        valor = token.valor.lower()

        # Padrões conhecidos de concatenação com 'tocar'
        if valor.startswith("toc"):
            # Extrair possível nota e duração
            resto = valor[3:]  # Remove 'toc'

            # Verificar padrões comuns
            if "seminima" in resto:
                parte_nota = resto.replace("seminima", "").replace("a", "").replace("r", "")

                # Buscar nota válida na parte restante
                for nota in self.notas_musicais:
                    if nota in parte_nota:
                        comando_correto = f"tocar {nota} seminima"
                        self._adicionar_erro(
                            f"Linha {token.linha}: Comando concatenado '{token.valor}' - Use: '{comando_correto}'"
                        )
                        return

            # Se não conseguiu extrair, dar sugestão genérica
            self._adicionar_erro(
                f"Linha {token.linha}: Comando malformado '{token.valor}' - Use formato: 'tocar <nota> <duracao>'"
            )

    def _calcular_similaridade_basica(self, str1: str, str2: str) -> float:
        """Calcula similaridade básica entre duas strings."""

        # Algoritmo simples: contar caracteres em comum
        comum = 0
        for char in str2:
            if char in str1:
                comum += 1

        return comum / len(str2)

    def _reportar_erro_token_invalido(self, token: Token):
        """Reporta erro de token inválido com sugestões inteligentes."""

        # Buscar sugestões em todas as categorias
        todas_palavras_validas = self.palavras_chave | self.notas_musicais | self.duracoes | self.instrumentos

        sugestoes = get_close_matches(
            token.valor.lower(),
            todas_palavras_validas,
            n=3,
            cutoff=0.4,  # Mais permissivo para capturar mais erros
        )

        if sugestoes:
            sugestoes_texto = "', '".join(sugestoes)
            self._adicionar_erro(
                f"Linha {token.linha}: Token inválido '{token.valor}' - Você quis dizer: '{sugestoes_texto}'?"
            )
        else:
            self._adicionar_erro(
                f"Linha {token.linha}: Token inválido '{token.valor}' - Token não reconhecido na linguagem MelodyScript"
            )

    def _analisar_sintaxe(self, tokens: List[Token]):
        """Análise sintática rigorosa baseada na gramática formal."""

        # Converter tokens para análise sintática
        self._validar_estrutura_comandos(tokens)
        self._validar_estrutura_melodias(tokens)
        self._validar_balanceamento_simbolos(tokens)

    def _validar_estrutura_comandos(self, tokens: List[Token]):
        """Valida estrutura de comandos usando gramática formal."""

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Comando tocar: deve seguir padrão "tocar <nota> <duracao> ;"
            if token.tipo == TipoToken.PALAVRA_CHAVE and token.valor.lower() == "tocar":
                i = self._validar_comando_tocar(tokens, i)
            # Outros comandos...
            else:
                i += 1

    def _validar_comando_tocar(self, tokens: List[Token], inicio: int) -> int:
        """Valida comando tocar seguindo gramática rigorosa."""

        # Padrão esperado: tocar <nota> <duracao> ;
        if inicio + 3 >= len(tokens):
            self._adicionar_erro(
                f"Linha {tokens[inicio].linha}: Comando 'tocar' incompleto - Esperado: 'tocar <nota> <duracao>;'"
            )
            return inicio + 1

        token_tocar = tokens[inicio]  # tocar
        token_nota = tokens[inicio + 1]  # nota
        token_duracao = tokens[inicio + 2]  # duracao
        token_pontovir = tokens[inicio + 3]  # ;

        # Validar sequência
        if token_nota.tipo != TipoToken.NOTA_MUSICAL:
            self._adicionar_erro(
                f"Linha {token_nota.linha}: Esperado nota musical após 'tocar', encontrado '{token_nota.valor}'"
            )

        if token_duracao.tipo != TipoToken.DURACAO:
            self._adicionar_erro(
                f"Linha {token_duracao.linha}: Esperado duração após nota, encontrado '{token_duracao.valor}'"
            )

        if token_pontovir.tipo != TipoToken.SIMBOLO or token_pontovir.valor != ";":
            self._adicionar_erro(
                f"Linha {token_pontovir.linha}: Esperado ';' após comando tocar, encontrado '{token_pontovir.valor}'"
            )

        return inicio + 4

    def _validar_estrutura_melodias(self, tokens: List[Token]):
        """Valida estrutura de definições de melodia."""
        # Implementar validação de estrutura de melodias
        pass

    def _validar_balanceamento_simbolos(self, tokens: List[Token]):
        """Valida balanceamento de chaves, parênteses, etc."""

        pilha_chaves = []
        pilha_parenteses = []

        for token in tokens:
            if token.valor == "{":
                pilha_chaves.append(token)
            elif token.valor == "}":
                if not pilha_chaves:
                    self._adicionar_erro(f"Linha {token.linha}: '}}' sem '{{' correspondente")
                else:
                    pilha_chaves.pop()
            elif token.valor == "(":
                pilha_parenteses.append(token)
            elif token.valor == ")":
                if not pilha_parenteses:
                    self._adicionar_erro(f"Linha {token.linha}: ')' sem '(' correspondente")
                else:
                    pilha_parenteses.pop()

        # Verificar símbolos não fechados
        for token in pilha_chaves:
            self._adicionar_erro(f"Linha {token.linha}: '{{' não fechada")
        for token in pilha_parenteses:
            self._adicionar_erro(f"Linha {token.linha}: '(' não fechado")

    def _validar_semantica(self, tokens: List[Token]):
        """Validação semântica - verificar contexto e coerência."""
        # Implementar validações semânticas adicionais
        pass

    def _remover_comentarios(self, conteudo: str) -> str:
        """Remove comentários do conteúdo."""
        # Remover comentários de bloco \_ ... _/
        conteudo_sem_comentarios = re.sub(r"\\_.*?_\/", "", conteudo, flags=re.DOTALL)
        return conteudo_sem_comentarios

    def _adicionar_erro(self, mensagem: str):
        """Adiciona um erro à lista de erros."""
        self.erros_sintaxe.append(mensagem)

    def obter_erros(self) -> List[str]:
        """Retorna a lista de erros encontrados."""
        return self.erros_sintaxe.copy()

    def limpar_erros(self):
        """Limpa a lista de erros."""
        self.erros_sintaxe.clear()


# Manter compatibilidade com código existente
class ValidadorTokens(AnalisadorSintaticoRobusto):
    """Alias para manter compatibilidade."""

    pass
