"""
Utilitários compartilhados para o linter MelodyScript.
Contém funções auxiliares usadas por diferentes módulos do linter.
"""

import re
from typing import List


def remover_comentarios(conteudo: str) -> str:
    """
    Remove os comentários do código MelodyScript para análise sintática.

    Args:
        conteudo: Conteúdo do código MelodyScript

    Returns:
        Conteúdo sem comentários
    """
    # Remover comentários no estilo \_ ... _/
    conteudo_sem_bloco = re.sub(r"\\_.*?_\/", "", conteudo)

    # Remover comentários no estilo # (linha)
    linhas = []
    for linha in conteudo_sem_bloco.split("\n"):
        # Verificar se o # não está dentro de uma nota musical (como do#)
        partes = re.split(r"(\s+)", linha)
        linha_processada = ""
        for parte in partes:
            if parte.strip() and parte.strip()[0] == "#":
                # É o início de um comentário
                break
            linha_processada += parte
        linhas.append(linha_processada)

    return "\n".join(linhas)


def verifica_parametro_funcao(nome: str) -> bool:
    """
    Verifica se um nome é provavelmente um parâmetro de função.

    Args:
        nome: Nome a ser verificado

    Returns:
        True se parece um parâmetro de função, False caso contrário
    """
    # Palavras comuns usadas como parâmetros de função
    parametros_comuns = [
        "duracao",
        "acorde",
        "nota",
        "tom",
        "tempo",
        "velocidade",
        "parametro",
        "valor",
        "freq",
        "frequencia",
        "oitava",
        "tonalidade",
        "volume",
        "intensidade",
    ]

    # Se o nome é uma dessas palavras específicas, é um parâmetro comum
    if nome.lower() in parametros_comuns:
        return True

    # Lista de durações válidas
    duracoes_validas = ["breve", "semibreve", "minima", "seminima", "colcheia", "semicolcheia", "fusa", "semifusa"]

    # Se o nome não é uma duração válida e é um identificador válido,
    # provavelmente é um parâmetro ou variável
    if nome not in duracoes_validas and re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", nome):
        # Verificar se poderia ser um identificador usado como parâmetro
        # Nomes curtos como um modificador (por exemplo "b") não devem ser considerados parâmetros
        if len(nome) > 1:
            return True

    return False


def obter_palavras_reservadas() -> List[str]:
    """
    Retorna a lista de palavras-chave reservadas da linguagem MelodyScript.

    Returns:
        Lista de palavras reservadas
    """
    return [
        "melodia",
        "tocar",
        "tocar_acorde",
        "pausa",
        "repetir",
        "vezes",
        "tempo",
        "instrumento",
        "forma_onda",
        "acorde",
        "envelope",
        "attack",
        "decay",
        "sustain",
        "release",
        "funcao",
        "retornar",
        "se",
        "senao",
        "configurar_envelope",
        "configurar_forma_onda",
        "para_cada",
        "em",
        "reverso",
    ]


def obter_erros_comuns() -> dict:
    """
    Retorna um dicionário com erros comuns de digitação e suas correções.

    Returns:
        Dicionário com erros comuns e correções
    """
    return {
        "tempu": "tempo",
        "tempoo": "tempo",
        "tiempo": "tempo",
        "repitir": "repetir",
        "veses": "vezes",
        "ves": "vezes",
        "instrumentu": "instrumento",
        "imstrumento": "instrumento",
        "envelope_config": "configurar_envelope",
        "tocaar": "tocar",
        "tokar": "tocar",
        "paausa": "pausa",
        "senão": "senao",
        "elso": "senao",
        "esle": "senao",
        "retornar": "retornar",
        "atacar": "attack",
        "decaimento": "decay",
        "sus": "sustain",
        "liberar": "release",
        "función": "funcao",
        "funcion": "funcao",
        "function": "funcao",
        "toke": "tocar",
        "toca": "tocar",
    }


def obter_duracoes_validas() -> List[str]:
    """
    Retorna a lista de durações válidas para notas musicais.

    Returns:
        Lista de durações válidas
    """
    return ["breve", "semibreve", "minima", "seminima", "colcheia", "semicolcheia", "fusa", "semifusa"]


def obter_formas_onda_validas() -> List[str]:
    """
    Retorna a lista de formas de onda válidas.

    Returns:
        Lista de formas de onda válidas
    """
    return ["sine", "square", "triangle", "sawtooth"]


def obter_funcoes_sistema() -> List[str]:
    """
    Retorna a lista de funções do sistema.

    Returns:
        Lista de funções do sistema
    """
    return ["tocar", "pausa", "transpor", "reverse", "reverso", "repetir"]
