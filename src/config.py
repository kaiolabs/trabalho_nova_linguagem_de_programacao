"""
Módulo de configuração para MelodyScript.
Lê configurações do arquivo config.ini ou de variáveis de ambiente.
"""

import configparser
import os
from pathlib import Path

# Caminho para o diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.parent

# Caminho para o arquivo de configuração
CONFIG_FILE = ROOT_DIR / "config.ini"

# Inicializar configuração com valores padrão
_config = configparser.ConfigParser()
_config["DEFAULT"] = {"DEBUG": "False", "VOLUME": "0.7", "VERBOSE": "False", "DEFAULT_EXAMPLES_DIR": "examples"}

# Carregar configurações do arquivo se existir
if CONFIG_FILE.exists():
    _config.read(CONFIG_FILE)


def get_config(key, default=""):
    """
    Obtém um valor de configuração.

    Args:
        key: A chave da configuração
        default: Valor padrão caso a chave não exista

    Returns:
        Valor da configuração (sempre uma string)
    """
    # Determinar ambiente
    environment = os.getenv("MELODYSCRIPT_ENV", "DEFAULT").upper()
    if environment not in _config:
        environment = "DEFAULT"

    # Verificar se a chave existe na seção do ambiente
    if key in _config[environment]:
        return str(_config[environment][key])

    # Verificar na seção DEFAULT
    if key in _config["DEFAULT"]:
        return str(_config["DEFAULT"][key])

    # Retornar valor padrão
    return str(default)


def is_debug_enabled():
    """
    Verifica se o modo de debug está ativado.

    Returns:
        True se o modo debug estiver ativado, False caso contrário
    """
    return get_config("DEBUG", "False").lower() in ("true", "1", "yes", "y")


def is_verbose_enabled():
    """
    Verifica se o modo verbose está ativado.

    Returns:
        True se o modo verbose estiver ativado, False caso contrário
    """
    return get_config("VERBOSE", "False").lower() in ("true", "1", "yes", "y")


def get_volume():
    """
    Obtém o valor do volume configurado.

    Returns:
        Valor do volume entre 0.0 e 1.0
    """
    try:
        volume = float(get_config("VOLUME", "0.7"))
        # Limitar entre 0.0 e 1.0
        return max(0.0, min(1.0, volume))
    except (ValueError, TypeError):
        return 0.7  # Valor padrão em caso de erro


def get_examples_dir():
    """
    Obtém o diretório de exemplos configurado.

    Returns:
        Caminho para o diretório de exemplos
    """
    return ROOT_DIR / get_config("DEFAULT_EXAMPLES_DIR", "examples")
