"""
Funções padrão da linguagem MelodyScript.
Define as funções predefinidas disponíveis na linguagem.
"""


def definir_funcoes_padrao():
    """
    Define as funções padrão da linguagem.

    Returns:
        Dicionário com as funções padrão
    """
    funcoes = {}

    # Função para calcular BPM
    funcoes["dobrar_tempo"] = {
        "params": ["valor"],
        "acao": lambda args, contexto: int(resolver_valor(args[0], contexto)) * 2,
        "descricao": "Calcula o dobro do valor de tempo fornecido.",
    }

    funcoes["metade_tempo"] = {
        "params": ["valor"],
        "acao": lambda args, contexto: int(resolver_valor(args[0], contexto)) / 2,
        "descricao": "Calcula a metade do valor de tempo fornecido.",
    }

    # Função para transpor notas
    funcoes["transpor"] = {
        "params": ["nota", "modificador", "semitons"],
        "acao": lambda args, contexto: {
            "tipo": "transpor",
            "nota": args[0],
            "modificador": args[1] if args[1] != "null" else None,
            "semitons": int(resolver_valor(args[2], contexto)),
        },
        "descricao": "Transpõe uma nota pelo número especificado de semitons.",
    }

    # Função para criar ritmos
    funcoes["repetir_padrao"] = {
        "params": ["padrao", "vezes"],
        "acao": lambda args, contexto: {
            "tipo": "repetir_padrao",
            "padrao": args[0],
            "vezes": int(resolver_valor(args[1], contexto)),
        },
        "descricao": "Repete um padrão musical o número especificado de vezes.",
    }

    return funcoes


def resolver_valor(valor, contexto):
    """
    Resolve o valor de um argumento, que pode ser uma variável ou um valor literal.

    Args:
        valor: String com o nome da variável ou valor literal
        contexto: Contexto de execução com as variáveis

    Returns:
        Valor resolvido
    """
    # String literal (entre aspas)
    if valor.startswith('"') and valor.endswith('"'):
        return valor[1:-1]  # Remove as aspas

    # Número literal
    try:
        if valor.isdigit():
            return int(valor)
        elif "." in valor and valor.replace(".", "", 1).isdigit():
            return float(valor)
    except (ValueError, AttributeError):
        pass  # Não é um número em formato de string

    # Verificar se é um nome de variável
    # 1. Verificar no escopo local
    if valor in contexto.escopo_atual:
        return contexto.escopo_atual[valor]

    # 2. Verificar no escopo global
    if valor in contexto.variaveis:
        return contexto.variaveis[valor]

    # 3. Verificar se é a variável 'tempo' definida no parser
    if valor == "tempo" and hasattr(contexto.parser, "tempo"):
        return contexto.parser.tempo

    # Se chegou aqui, retorna o valor original
    return valor
