"""
Processador central de comandos da linguagem MelodyScript.
Coordena o processamento de diferentes tipos de comandos.
"""

from src.linguagem.comandos.comandos_estruturas import ComandosEstruturas
from src.linguagem.comandos.comandos_simples import ComandosSimples


class ProcessadorComandos:
    """Processador de comandos da linguagem MelodyScript."""

    def __init__(self, parser):
        """
        Inicializa o processador de comandos.

        Args:
            parser: Instância do parser principal
        """
        self.parser = parser
        self.comandos_simples = ComandosSimples(self)
        self.comandos_estruturas = ComandosEstruturas(self)

    def processar_comandos_melodia(self, conteudo, comandos):
        """
        Processa os comandos dentro de uma melodia.

        Args:
            conteudo: String com o conteúdo da melodia
            comandos: Lista onde os comandos serão adicionados
        """
        pos_inicial = 0

        # Encontrar e processar blocos paralelos
        pos_inicial = self.comandos_estruturas.processar_blocos_paralelos(conteudo, comandos, pos_inicial)

        # Encontrar e processar estruturas condicionais
        pos_inicial = self.comandos_estruturas.processar_condicionais(conteudo, comandos, pos_inicial)

        # Encontrar e processar iterações "para cada"
        pos_inicial = self.comandos_estruturas.processar_para_cada(conteudo, comandos, pos_inicial)

        # Encontrar e processar repetições
        pos_inicial = self.comandos_estruturas.processar_repeticoes(conteudo, comandos, pos_inicial)

        # Processar os comandos após a última estrutura especial
        self.processar_comandos_simples(conteudo[pos_inicial:], comandos)

    def processar_comandos_simples(self, conteudo, comandos):
        """
        Processa comandos simples (tocar, pausa, configurações) usando a classe ComandosSimples.

        Args:
            conteudo: String com o conteúdo a ser processado
            comandos: Lista onde os comandos serão adicionados
        """
        self.comandos_simples.processar(conteudo, comandos)
