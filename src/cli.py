"""
Interface de linha de comando para a MelodyScript.
"""

import argparse
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para permitir importações relativas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import is_debug_enabled, is_verbose_enabled
from src.core.interpretador import MelodyScriptInterpretador
from src.linter import MelodyScriptLinter


def main():
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(description="Interpretador MelodyScript")
    parser.add_argument("comando", choices=["executar", "validar"], help="Comando a executar")
    parser.add_argument("arquivo", help="Arquivo .mscr para processar")
    parser.add_argument("--melodia", help="Nome da melodia a executar (opcional)")
    parser.add_argument("--debug", action="store_true", help="Ativar modo de depuração")
    parser.add_argument("--env", help="Ambiente de configuração a usar (default, development, production)")

    args = parser.parse_args()

    # Definir o ambiente baseado no argumento --env ou na variável de ambiente
    if args.env:
        os.environ["MELODYSCRIPT_ENV"] = args.env.upper()

    # Configuração para ativar o modo debug se for solicitado por argumento,
    # independente da configuração no arquivo
    debug_mode = args.debug or is_debug_enabled()
    verbose_mode = is_verbose_enabled()

    if debug_mode:
        print("Modo de depuração ativado")

    if verbose_mode:
        print(f"Ambiente: {os.getenv('MELODYSCRIPT_ENV', 'DEFAULT')}")
        print(f"Configurações carregadas do arquivo: {Path(__file__).parent.parent / 'config.ini'}")

    # Verificar extensão do arquivo
    if not args.arquivo.endswith(".mscr"):
        print("Erro: O arquivo deve ter a extensão .mscr")
        return 1

    if args.comando == "executar":
        # Executar o arquivo
        interpretador = MelodyScriptInterpretador()
        interpretador.debug_mode = debug_mode

        if interpretador.carregar_arquivo(args.arquivo):
            # Se uma melodia específica foi solicitada, use-a
            # Caso contrário, mostre as melodias disponíveis e use a primeira
            if not args.melodia and interpretador.parser.melodias:
                if verbose_mode:
                    print("Melodias disponíveis:")
                    for nome in interpretador.parser.melodias.keys():
                        print(f"  - {nome}")
                # Usar a primeira melodia
                melodia_para_executar = list(interpretador.parser.melodias.keys())[0]
                if verbose_mode:
                    print(f"Usando a melodia: {melodia_para_executar}")
                interpretador.executar_melodia(melodia_para_executar)
            else:
                interpretador.executar_melodia(args.melodia)
        else:
            return 1
    elif args.comando == "validar":
        # Validar o arquivo
        linter = MelodyScriptLinter()
        linter.debug_mode = debug_mode
        if not linter.validar_arquivo(args.arquivo):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
