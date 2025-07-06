"""
Módulo de utilitários do MelodyScript.
Contém funções e classes auxiliares usadas por outros módulos.
"""

from src.utils.teoria_musical import (
    ACORDES,
    DURACOES,
    MODIFICADORES,
    NOTAS,
    calcular_duracao,
    calcular_frequencia,
    calcular_frequencias_acorde,
    indice_para_frequencia,
    nota_para_indice,
)

__all__ = [
    "calcular_duracao",
    "calcular_frequencia",
    "calcular_frequencias_acorde",
    "nota_para_indice",
    "indice_para_frequencia",
    "NOTAS",
    "MODIFICADORES",
    "DURACOES",
    "ACORDES",
]
