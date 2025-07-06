#!/bin/bash
# Script para executar a MelodyScript com o ambiente virtual

# Obter o diretório atual do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Ativando ambiente virtual em $SCRIPT_DIR/.venv"

# Ativar o ambiente virtual
source "$SCRIPT_DIR/.venv/bin/activate"

# Verificar se o ambiente está ativado corretamente
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "ERRO: Ambiente virtual não foi ativado corretamente!"
    echo "Tentando método alternativo..."
    # Método alternativo para ativar o ambiente
    PATH="$SCRIPT_DIR/.venv/bin:$PATH"
    export PATH
    echo "PATH atualizado para: $PATH"
fi

echo "Usando Python: $(which python)"
echo "Versão Python: $(python --version)"

# Executar o comando MelodyScript
if [ "$1" = "executar" ]; then
    echo "Executando: python -m src.melodyscript executar \"$2\""
    python -m src.melodyscript executar "$2"
elif [ "$1" = "validar" ]; then
    echo "Validando: python -m src.melodyscript validar \"$2\""
    python -m src.melodyscript validar "$2"
else
    echo "Uso: $0 [executar|validar] arquivo.mscr"
    exit 1
fi 