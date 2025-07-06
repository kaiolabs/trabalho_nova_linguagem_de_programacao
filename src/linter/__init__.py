"""
Linter para a linguagem MelodyScript.
Módulo modular para verificação de sintaxe e semântica do código MelodyScript.
"""

from .cli import main
from .core import MelodyScriptLinter

__version__ = "1.0.0"
__all__ = ["MelodyScriptLinter", "main"]
