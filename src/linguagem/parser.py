"""
Parser para a linguagem MelodyScript.
Responsável por analisar o código fonte e transformá-lo em uma estrutura de dados.
"""

from src.linguagem.comandos import ProcessadorComandos
from src.linguagem.funcoes_padrao import definir_funcoes_padrao
from src.linguagem.parser_definicoes import ProcessadorDefinicoes


class MelodyScriptParser:
    """Parser para a linguagem MelodyScript."""

    def __init__(self):
        """Inicializa o parser."""
        self._debug_mode = False  # Modo de debug padrão desligado
        self.reset()
        self.processador_definicoes = ProcessadorDefinicoes(self)
        self.processador_comandos = ProcessadorComandos(self)

    def reset(self):
        """Reseta o estado do parser."""
        self.tempo = 120  # BPM padrão
        self.instrumento = "piano"  # Instrumento padrão
        self.melodias = {}
        self.acordes = {}
        self.variaveis = {}
        self.funcoes = definir_funcoes_padrao()  # Carregar funções predefinidas

        # Configurações de som
        self.envelope = {}
        self.waveform = ""

        # Configuração para reprodução paralela (padrão: desativada)
        self.modo_paralelo = False

    @property
    def debug_mode(self):
        """Getter para o modo de debug."""
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        """Setter para o modo de debug."""
        self._debug_mode = bool(value)

    def parsear_arquivo(self, caminho):
        """
        Faz o parsing de um arquivo MelodyScript.

        Args:
            caminho: Caminho para o arquivo a ser parseado

        Returns:
            True se o parsing foi bem-sucedido, False caso contrário
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()

            # DEBUG: Mostrar o conteúdo original
            if self._debug_mode:
                print("DEBUG: Conteúdo original do arquivo:")
                print("-----------------------------------")
                print(conteudo)
                print("-----------------------------------")

            # Processar o conteúdo do arquivo
            self._processar_conteudo(conteudo)

            # DEBUG: Mostrar melodias encontradas
            if self._debug_mode:
                print("DEBUG: Melodias encontradas:")
                for nome, comandos in self.melodias.items():
                    print(f"  - {nome}: {len(comandos)} comandos")

            return True

        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            return False

    def _processar_conteudo(self, conteudo):
        """
        Processa o conteúdo completo do arquivo.

        Args:
            conteudo: String com o conteúdo do arquivo
        """
        # Remover comentários de linha (novo estilo \_ ... _/)
        import re

        conteudo_sem_comentarios = re.sub(r"\\_.*?_\/", "", conteudo)

        # Preservar comentários antigos (# no início da linha) para compatibilidade
        linhas = []
        for linha in conteudo_sem_comentarios.split("\n"):
            if "#" in linha:
                # Verificar se o # não está dentro de uma nota musical (como do#)
                partes = re.split(r"(\s+)", linha)
                linha_processada = ""
                for parte in partes:
                    if parte.strip() and parte.strip()[0] == "#":
                        # É o início de um comentário
                        break
                    linha_processada += parte
                linhas.append(linha_processada.strip())
            else:
                linhas.append(linha.strip())

        # Juntar linhas e remover espaços desnecessários
        conteudo_limpo = " ".join([linha for linha in linhas if linha])

        # DEBUG: Mostrar o conteúdo limpo
        if self._debug_mode:
            print("DEBUG: Conteúdo após processamento inicial:")
            print("-----------------------------------")
            print(conteudo_limpo)
            print("-----------------------------------")

        # Verificar se o modo paralelo está habilitado
        modo_paralelo_pattern = r"modo_paralelo\s+(true|verdadeiro|sim|1|on|ativado)"
        self.modo_paralelo = bool(re.search(modo_paralelo_pattern, conteudo_limpo, re.IGNORECASE))

        if self._debug_mode:
            print(f"DEBUG: Modo paralelo: {'Ativado' if self.modo_paralelo else 'Desativado'}")

        # Processar definições globais (tempo, instrumento, envelope, forma de onda)
        self.processador_definicoes.processar_definicoes_globais(conteudo_limpo)

        # Processar definições de acordes
        self.processador_definicoes.processar_definicoes_acordes(conteudo_limpo)

        # Processar definições de funções
        self.processador_definicoes.processar_definicoes_funcoes(conteudo_limpo)

        # Processar melodias
        self.processador_definicoes.processar_melodias(conteudo_limpo)
