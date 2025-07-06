#!/bin/bash
# Script para configuração do ambiente de desenvolvimento da MelodyScript

echo "Configurando ambiente de desenvolvimento para MelodyScript..."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Por favor, instale o Python 3."
    exit 1
fi

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv .venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

echo "Ambiente de desenvolvimento configurado com sucesso!"
echo "Para ativar o ambiente virtual, execute:"
echo "source .venv/bin/activate"

echo "Para executar o exemplo 'Olá Mundo', ative o ambiente virtual e digite:"
echo "python3 src/melodyscript.py executar examples/ola_mundo.mscr" 