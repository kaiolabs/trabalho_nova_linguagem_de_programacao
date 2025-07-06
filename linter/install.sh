#!/bin/bash
# Script para instalar a extensão MelodyScript para VSCode

echo "Instalando a extensão MelodyScript no VSCode..."

# Verificar se o código VSCode está instalado
if ! command -v code &> /dev/null; then
    echo "Erro: VSCode não encontrado. Por favor, instale o VSCode primeiro."
    echo "Visite https://code.visualstudio.com/download para instruções de instalação."
    exit 1
fi

# Diretório do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Caminho para o arquivo VSIX
VSIX_PATH="$SCRIPT_DIR/melodyscript-language-0.1.0.vsix"

# Verificar se o arquivo VSIX existe
if [ ! -f "$VSIX_PATH" ]; then
    echo "Erro: Arquivo VSIX não encontrado em $VSIX_PATH"
    echo "Execute 'cd $SCRIPT_DIR && npm run package' para gerar o arquivo VSIX primeiro."
    exit 1
fi

# Instalar a extensão
echo "Instalando a extensão a partir de $VSIX_PATH..."
code --install-extension "$VSIX_PATH"

# Verificar se a instalação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Extensão MelodyScript instalada com sucesso!"
    echo "Reinicie o VSCode para aplicar as alterações."
else
    echo "Erro ao instalar a extensão. Verifique as mensagens de erro acima."
    exit 1
fi 