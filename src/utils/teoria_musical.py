"""
Teoria musical para a MelodyScript.
Define constantes e funções relacionadas à notação musical.
"""

# Mapeamento de notas para frequências (Hz) - baseado na escala temperada
NOTAS = {
    # Notas em português
    "do": 261.63,  # C4 (Dó central)
    "re": 293.66,  # D4 (Ré)
    "mi": 329.63,  # E4 (Mi)
    "fa": 349.23,  # F4 (Fá)
    "sol": 392.00,  # G4 (Sol)
    "la": 440.00,  # A4 (Lá)
    "si": 493.88,  # B4 (Si)
    # Suporte a nomes alternativos (incluindo notação inglesa)
    "c": 261.63,  # C4
    "d": 293.66,  # D4
    "e": 329.63,  # E4
    "f": 349.23,  # F4
    "g": 392.00,  # G4
    "a": 440.00,  # A4
    "b": 493.88,  # B4
    # Notas com oitavas específicas - Oitava 1 (2 oitavas abaixo da oitava central)
    "do1": 32.70,  # C1
    "re1": 36.71,  # D1
    "mi1": 41.20,  # E1
    "fa1": 43.65,  # F1
    "sol1": 49.00,  # G1
    "la1": 55.00,  # A1
    "si1": 61.74,  # B1
    # Oitava 2 (1 oitava abaixo da oitava central)
    "do2": 65.41,  # C2
    "re2": 73.42,  # D2
    "mi2": 82.41,  # E2
    "fa2": 87.31,  # F2
    "sol2": 98.00,  # G2
    "la2": 110.00,  # A2
    "si2": 123.47,  # B2
    # Oitava 3 (abaixo da oitava central)
    "do3": 130.81,  # C3
    "re3": 146.83,  # D3
    "mi3": 164.81,  # E3
    "fa3": 174.61,  # F3
    "sol3": 196.00,  # G3
    "la3": 220.00,  # A3
    "si3": 246.94,  # B3
    # Oitava 4 (oitava central)
    "do4": 261.63,  # C4 (Dó central)
    "re4": 293.66,  # D4
    "mi4": 329.63,  # E4
    "fa4": 349.23,  # F4
    "sol4": 392.00,  # G4
    "la4": 440.00,  # A4
    "si4": 493.88,  # B4
    # Oitava 5 (acima da oitava central)
    "do5": 523.25,  # C5
    "re5": 587.33,  # D5
    "mi5": 659.25,  # E5
    "fa5": 698.46,  # F5
    "sol5": 783.99,  # G5
    "la5": 880.00,  # A5
    "si5": 987.77,  # B5
    # Oitava 6 (2 oitavas acima da oitava central)
    "do6": 1046.50,  # C6
    "re6": 1174.66,  # D6
    "mi6": 1318.51,  # E6
    "fa6": 1396.91,  # F6
    "sol6": 1567.98,  # G6
    "la6": 1760.00,  # A6
    "si6": 1975.53,  # B6
    # Oitava 7 (3 oitavas acima da oitava central)
    "do7": 2093.00,  # C7
    "re7": 2349.32,  # D7
    "mi7": 2637.02,  # E7
    "fa7": 2793.83,  # F7
    "sol7": 3135.96,  # G7
    "la7": 3520.00,  # A7
    "si7": 3951.07,  # B7
}

# Mapeamento de modificadores (sustenido e bemol)
MODIFICADORES = {
    "#": 1.059463,  # Aumenta a frequência por um semitom (razão de 2^(1/12))
    "b": 0.943874,  # Diminui a frequência por um semitom (razão de 2^(-1/12))
}

# Mapeamento de durações para valores relativos de tempo
DURACOES = {
    "breve": 4.0,  # Quatro tempos
    "semibreve": 2.0,  # Dois tempos
    "minima": 1.0,  # Um tempo
    "seminima": 0.5,  # Meio tempo
    "colcheia": 0.25,  # Um quarto de tempo
    "semicolcheia": 0.125,  # Um oitavo de tempo
}

# Definições de estruturas de acordes comuns
ACORDES = {
    "maior": [0, 4, 7],  # Tríade maior (ex: Do-Mi-Sol)
    "menor": [0, 3, 7],  # Tríade menor (ex: Do-Mib-Sol)
    "aumentado": [0, 4, 8],  # Tríade aumentada (ex: Do-Mi-Sol#)
    "diminuto": [0, 3, 6],  # Tríade diminuta (ex: Do-Mib-Solb)
    "maior7": [0, 4, 7, 11],  # Acorde de sétima maior (ex: Do-Mi-Sol-Si)
    "menor7": [0, 3, 7, 10],  # Acorde de sétima menor (ex: Do-Mib-Sol-Sib)
    "dominante7": [0, 4, 7, 10],  # Acorde de sétima dominante (ex: Do-Mi-Sol-Sib)
}


def calcular_frequencia(nota, modificador=None):
    """
    Calcula a frequência de uma nota musical.

    Args:
        nota: Nome da nota (do, re, mi, etc.) com oitava opcional (do4, mi5)
        modificador: Modificador opcional (# ou b)

    Returns:
        Frequência da nota em Hz
    """
    # Converter para minúsculo para garantir consistência
    nota_lower = nota.lower()

    # Verificar se existe diretamente no dicionário de notas
    if nota_lower in NOTAS:
        frequencia_base = NOTAS[nota_lower]
    else:
        # Verifica se a nota tem um número de oitava no final (ex: "do#4")
        # Para notas como "do#4", precisamos extrair a nota base antes de processar oitava
        nota_base = "".join([c for c in nota_lower if not c.isdigit()])

        # Extrair os dígitos ao final da string (representa a oitava)
        digitos = "".join([c for c in nota_lower if c.isdigit()])

        if digitos and nota_base in NOTAS:
            # Se temos apenas dígitos da oitava e a nota base é válida,
            # calculamos a frequência baseada na nota padrão e ajustamos para a oitava
            oitava = int(digitos)
            oitava_padrao = 4  # Oitava padrão para notas sem número

            # Frequência da nota base (sem oitava)
            freq_nota_base = NOTAS[nota_base]

            # Cálculo da diferença de oitavas: cada oitava dobra a frequência
            diferenca_oitavas = oitava - oitava_padrao

            # Ajuste da frequência base de acordo com a diferença de oitavas
            frequencia_base = freq_nota_base * (2**diferenca_oitavas)
        else:
            # Caso não encontre, usar A4 (lá) como padrão
            print(f"Aviso: Nota '{nota}' não reconhecida. Usando 'lá' (A4) como substituto.")
            frequencia_base = 440.0

    # Aplicar modificador se existir
    if modificador:
        if modificador in MODIFICADORES:
            fator = MODIFICADORES[modificador]
            frequencia_base *= fator
        else:
            print(f"Aviso: Modificador '{modificador}' não reconhecido. Ignorando modificador.")

    return frequencia_base


def calcular_duracao(nome_duracao, bpm):
    """
    Calcula a duração real em segundos de uma nota musical.

    Args:
        nome_duracao: Nome da duração (seminima, minima, etc.)
        bpm: Andamento em batidas por minuto

    Returns:
        Duração em segundos
    """
    # Converter para minúsculo para garantir consistência
    duracao_lower = nome_duracao.lower()

    # Calcular a duração de uma batida em segundos
    beat_duration = 60.0 / bpm

    # Obter o valor relativo da duração ou usar seminima como padrão
    if duracao_lower in DURACOES:
        duracao_relativa = DURACOES[duracao_lower]
    else:
        print(f"Aviso: Duração '{nome_duracao}' não reconhecida. Usando 'seminima' como substituto.")
        duracao_relativa = 0.5  # Valor da seminima

    # Calcular a duração em segundos
    # O fator 2 é um ajuste sonoro para melhorar a percepção das durações
    return duracao_relativa * beat_duration * 2


def calcular_frequencias_acorde(nota_base, tipo_acorde, modificador=None):
    """
    Calcula as frequências de todas as notas de um acorde.

    Args:
        nota_base: Nome da nota base (do, re, mi, etc.)
        tipo_acorde: Tipo do acorde (maior, menor, etc.)
        modificador: Modificador opcional da nota base (# ou b)

    Returns:
        Lista de frequências em Hz das notas do acorde
    """
    # Calcular a frequência da nota base
    freq_base = calcular_frequencia(nota_base, modificador)

    # Verificar se o tipo de acorde é conhecido
    if tipo_acorde.lower() not in ACORDES:
        print(f"Aviso: Tipo de acorde '{tipo_acorde}' não reconhecido. Usando acorde maior como substituto.")
        intervalos = ACORDES["maior"]
    else:
        intervalos = ACORDES[tipo_acorde.lower()]

    # Calcular todas as frequências do acorde
    frequencias = []
    for intervalo in intervalos:
        # Cada semitom representa um fator de 2^(1/12)
        frequencia = freq_base * (2 ** (intervalo / 12))
        frequencias.append(frequencia)

    return frequencias


def nota_para_indice(nota, modificador=None):
    """
    Converte uma nota musical para um índice MIDI relativo.

    Args:
        nota: Nome da nota (do, re, mi, etc.)
        modificador: Modificador opcional (# ou b)

    Returns:
        Índice MIDI relativo da nota
    """
    indices_base = {
        "do": 0,
        "c": 0,
        "re": 2,
        "d": 2,
        "mi": 4,
        "e": 4,
        "fa": 5,
        "f": 5,
        "sol": 7,
        "g": 7,
        "la": 9,
        "a": 9,
        "si": 11,
        "b": 11,
    }

    # Converter para minúsculo para garantir consistência
    nota_lower = nota.lower()

    # Extrair oitava se presente
    digitos = "".join([c for c in nota_lower if c.isdigit()])
    nota_sem_oitava = "".join([c for c in nota_lower if not c.isdigit()])

    # Obter o índice base da nota
    indice = indices_base.get(nota_sem_oitava, 0)

    # Aplicar modificador se existir
    if modificador:
        if modificador == "#":
            indice += 1
        elif modificador == "b":
            indice -= 1

    # Ajustar para a oitava específica, se fornecida
    if digitos:
        oitava = int(digitos)
        indice = (oitava + 1) * 12 + indice

    return indice


def indice_para_frequencia(indice):
    """
    Converte um índice MIDI relativo para frequência.
    Usando A4 (Lá, 440Hz) como referência.

    Args:
        indice: Índice MIDI relativo da nota

    Returns:
        Frequência correspondente em Hz
    """
    # A nota A4 (Lá) tem MIDI relativo 69 e frequência 440Hz
    # Cada semitom é um fator de 2^(1/12)
    indice_a4 = 69
    frequencia_a4 = 440.0

    return frequencia_a4 * (2 ** ((indice - indice_a4) / 12))
