#!/bin/bash
# Script para recompilar a extensão VSCode MelodyScript

echo "Recompilando a extensão VSCode MelodyScript..."

# Obter o diretório atual do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navegar para o diretório da extensão
cd "$SCRIPT_DIR/linter"

# Verificar se npm está instalado
if ! command -v npm &> /dev/null; then
    echo "Erro: npm não encontrado. Por favor, instale o Node.js e npm primeiro."
    exit 1
fi

# Instalar dependências, se necessário
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências..."
    npm install
fi

# Garantir que @vscode/vsce esteja instalado como dependência de desenvolvimento
if ! grep -q "@vscode/vsce" package.json; then
    echo "Adicionando @vscode/vsce como dependência de desenvolvimento..."
    npm install --save-dev @vscode/vsce
fi

# Compilar a extensão
echo "Compilando a extensão..."
npm run compile

# Verificar se a compilação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "✅ Extensão compilada com sucesso!"
    
    # Empacotar a extensão em um arquivo VSIX
    echo "Empacotando a extensão em VSIX..."
    npx vsce package
    
    if [ $? -eq 0 ]; then
        echo "✅ Arquivo VSIX criado com sucesso!"
        echo "O arquivo VSIX está disponível em: $SCRIPT_DIR/linter/melodyscript-language-0.1.0.vsix"
        echo "Para instalar a extensão, use o comando 'code --install-extension melodyscript-language-0.1.0.vsix' ou instale manualmente pelo VSCode."
    else
        echo "❌ Erro ao criar o arquivo VSIX. Verifique as mensagens de erro acima."
        exit 1
    fi
else
    echo "❌ Erro ao compilar a extensão. Verifique as mensagens de erro acima."
    exit 1
fi 