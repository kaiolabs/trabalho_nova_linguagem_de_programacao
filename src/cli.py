"""
Interface de linha de comando para MelodyScript.
"""

import argparse
import sys
from pathlib import Path

from src.core.interpretador import MelodyScriptInterpretador
from src.linguagem.parser import MelodyScriptParser


def main():
    """Função principal do CLI."""
    parser = argparse.ArgumentParser(
        description="MelodyScript - Linguagem de programação para criação de música",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  melodyscript executar arquivo.mscr           # Executa um arquivo MelodyScript
  melodyscript executar arquivo.mscr --debug   # Executa com modo debug ativado
  melodyscript lint arquivo.mscr               # Verifica sintaxe sem executar
        """,
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")

    # Comando executar
    parser_executar = subparsers.add_parser("executar", help="Executa um arquivo MelodyScript")
    parser_executar.add_argument("arquivo", help="Caminho para o arquivo .mscr")
    parser_executar.add_argument("--debug", action="store_true", help="Ativa o modo debug")

    # Comando lint
    parser_lint = subparsers.add_parser("lint", help="Verifica a sintaxe de um arquivo MelodyScript")
    parser_lint.add_argument("arquivo", help="Caminho para o arquivo .mscr")

    args = parser.parse_args()

    if not args.comando:
        parser.print_help()
        return

    # Verificar se o arquivo existe
    arquivo_path = Path(args.arquivo)
    if not arquivo_path.exists():
        print(f"\033[91m❌ Erro: Arquivo '{args.arquivo}' não encontrado.\033[0m")
        sys.exit(1)

    if args.comando == "executar":
        executar_arquivo(args.arquivo, args.debug)
    elif args.comando == "lint":
        lint_arquivo(args.arquivo)


def executar_arquivo(caminho_arquivo, debug=False):
    """
    Executa um arquivo MelodyScript.

    Args:
        caminho_arquivo: Caminho para o arquivo a ser executado
        debug: Se True, ativa o modo debug
    """
    print(f"🎵 MelodyScript - Executando arquivo: {caminho_arquivo}")
    print("=" * 60)

    try:
        # Criar interpretador
        interpretador = MelodyScriptInterpretador()
        interpretador.debug_mode = debug

        # Carregar e parsear arquivo (inclui validação completa)
        if not interpretador.carregar_arquivo(caminho_arquivo):
            print("\033[91m❌ Falha na compilação. Execução cancelada.\033[0m")
            sys.exit(1)

        # Verificação adicional de segurança
        if (
            interpretador.parser.processador_comandos.tem_erros_sintaxe()
            or interpretador.parser.validador_tokens.obter_erros()
        ):
            print("\033[91m❌ Erros de sintaxe detectados. Execução cancelada devido a erros de sintaxe.\033[0m")
            sys.exit(1)

        # Executar a primeira melodia encontrada
        print("\n🎼 Iniciando execução da música...")
        if interpretador.executar_melodia():
            print("\n✅ Execução concluída com sucesso!")
        else:
            print("\n❌ Erro durante a execução da melodia.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Execução interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\033[91m❌ Erro durante a execução: {e}\033[0m")
        sys.exit(1)


def lint_arquivo(caminho_arquivo):
    """
    Verifica a sintaxe de um arquivo MelodyScript sem executar.

    Args:
        caminho_arquivo: Caminho para o arquivo a ser verificado
    """
    print(f"🔍 MelodyScript Linter - Verificando arquivo: {caminho_arquivo}")
    print("=" * 60)

    try:
        # Criar parser
        parser = MelodyScriptParser()
        parser.debug_mode = False

        # Fazer parsing do arquivo (inclui validação completa)
        if parser.parsear_arquivo(caminho_arquivo):
            print("\n✅ Arquivo válido! Nenhum erro de sintaxe encontrado.")

            # Mostrar estatísticas
            num_melodias = len(parser.melodias)
            num_acordes = len(parser.acordes)
            num_funcoes = len(parser.funcoes) - len(parser.funcoes)  # Subtrair funções predefinidas

            print("\n📊 Estatísticas do arquivo:")
            print(f"   • Melodias definidas: {num_melodias}")
            print(f"   • Acordes definidos: {num_acordes}")
            print(f"   • Funções definidas: {num_funcoes}")
            print(f"   • Tempo: {parser.tempo} BPM")
            print(f"   • Instrumento padrão: {parser.instrumento}")

            if parser.modo_paralelo:
                print("   • Modo paralelo: Ativado")

            sys.exit(0)
        else:
            print("\n❌ Arquivo inválido! Corrija os erros antes de executar.")
            sys.exit(1)

    except Exception as e:
        print(f"\033[91m❌ Erro durante a verificação: {e}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
