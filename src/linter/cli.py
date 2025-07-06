"""
Interface de linha de comando para o linter MelodyScript.
Fornece funcionalidade de CLI para validação de arquivos.
"""

import argparse

from .core import MelodyScriptLinter


def main():
    """Função principal para execução do linter como script."""
    parser = argparse.ArgumentParser(description="MelodyScript Linter - Validador de código MelodyScript")
    parser.add_argument("arquivo", help="Caminho para o arquivo .mscr a ser validado")
    parser.add_argument("-d", "--debug", action="store_true", help="Ativar modo de debug")

    args = parser.parse_args()

    linter = MelodyScriptLinter()
    linter.debug_mode = args.debug

    # Executar validação
    sucesso = linter.validar_arquivo(args.arquivo)

    # Sair com código apropriado
    exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
