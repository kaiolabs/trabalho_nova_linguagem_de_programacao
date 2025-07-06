"""
Classe principal do linter MelodyScript.
Orquestra todos os verificadores (sintaxe, semântica, balanceamento).
"""

from .balance_checker import BalanceChecker
from .semantic_checker import SemanticChecker
from .simple_syntax_checker import SimpleSyntaxChecker


class MelodyScriptLinter:
    """Linter principal para a linguagem MelodyScript."""

    def __init__(self):
        """Inicializa o linter principal."""
        self._debug_mode = False
        self.erros = []
        self.avisos = []

    @property
    def debug_mode(self):
        """Getter para o modo de debug."""
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        """Setter para o modo de debug."""
        self._debug_mode = bool(value)

    def validar_arquivo(self, caminho: str) -> bool:
        """
        Valida um arquivo MelodyScript completo.

        Args:
            caminho: Caminho para o arquivo a ser validado

        Returns:
            True se o arquivo é válido, False caso contrário
        """
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")
            return False

        return self.validar_conteudo(conteudo, caminho)

    def validar_conteudo(self, conteudo: str, nome_arquivo: str = "") -> bool:
        """
        Valida o conteúdo de um arquivo MelodyScript.

        Args:
            conteudo: Conteúdo do arquivo MelodyScript
            nome_arquivo: Nome do arquivo (opcional, para mensagens)

        Returns:
            True se o conteúdo é válido, False caso contrário
        """
        # Reiniciar listas de erros e avisos
        self.erros = []
        self.avisos = []

        # Criar instâncias dos verificadores
        balance_checker = BalanceChecker(self._debug_mode)
        semantic_checker = SemanticChecker(self._debug_mode)
        syntax_checker = SimpleSyntaxChecker(self._debug_mode)

        # Verificar balanceamento
        erros_balanceamento = balance_checker.verificar_balanceamento(conteudo)
        self.erros.extend(erros_balanceamento)

        # Verificar sintaxe
        erros_sintaxe, avisos_sintaxe = syntax_checker.verificar_sintaxe(conteudo)
        self.erros.extend(erros_sintaxe)
        self.avisos.extend(avisos_sintaxe)

        # Verificar semântica (apenas avisos)
        avisos_semantica = semantic_checker.verificar_semantica(conteudo)
        self.avisos.extend(avisos_semantica)

        # Exibir resultados da validação
        self._exibir_resultados(nome_arquivo, conteudo)

        return not self.erros  # Válido se não houver erros

    def _exibir_resultados(self, nome_arquivo: str, conteudo: str) -> None:
        """
        Exibe os resultados da validação.

        Args:
            nome_arquivo: Nome do arquivo validado
            conteudo: Conteúdo do arquivo (para debug)
        """
        arquivo_nome = nome_arquivo or "arquivo"

        if not self.erros and not self.avisos:
            print(f"{arquivo_nome} é válido.")
            return

        if self.erros:
            # Debug: Mostrar linhas específicas com erro
            if self._debug_mode:
                print("\nDebug de linhas com erro:")
                linhas = conteudo.split("\n")
                for erro in self.erros:
                    if "Linha " in erro:
                        try:
                            num_linha = int(erro.split("Linha ")[1].split(":")[0])
                            if 1 <= num_linha <= len(linhas):
                                print(f"  Linha {num_linha}: '{linhas[num_linha - 1].strip()}'")
                        except (ValueError, IndexError):
                            pass
                print()

            print(f"Encontrados {len(self.erros)} erros:")
            for erro in self.erros:
                print(f"  - {erro}")

        if self.avisos:
            print(f"Encontrados {len(self.avisos)} avisos:")
            for aviso in self.avisos:
                print(f"  - {aviso}")
