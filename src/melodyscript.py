#!/usr/bin/env python3
"""
MelodyScript - Um interpretador para a linguagem de programação musical MelodyScript.
Este arquivo serve como ponto de entrada para o interpretador.
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para permitir importações relativas
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli import main

if __name__ == "__main__":
    main()
