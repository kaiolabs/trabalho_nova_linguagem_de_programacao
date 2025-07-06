@echo off
REM Script para recompilar a extensão VSCode MelodyScript no Windows

echo Recompilando a extensão VSCode MelodyScript...

REM Obter o diretório atual do script
set SCRIPT_DIR=%~dp0
set LINTER_DIR=%SCRIPT_DIR%linter

REM Navegar para o diretório da extensão
cd /d "%LINTER_DIR%"

REM Verificar se npm está instalado
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erro: npm não encontrado. Por favor, instale o Node.js e npm primeiro.
    exit /b 1
)

REM Instalar dependências, se necessário
if not exist "node_modules" (
    echo Instalando dependências...
    call npm install
)

REM Garantir que @vscode/vsce esteja instalado como dependência de desenvolvimento
findstr "@vscode/vsce" package.json >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Adicionando @vscode/vsce como dependência de desenvolvimento...
    call npm install --save-dev @vscode/vsce
)

REM Compilar a extensão
echo Compilando a extensão...
call npm run compile

REM Verificar se a compilação foi bem-sucedida
if %ERRORLEVEL% EQU 0 (
    echo ✅ Extensão compilada com sucesso!
    
    REM Empacotar a extensão em um arquivo VSIX
    echo Empacotando a extensão em VSIX...
    call npx vsce package
    
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Arquivo VSIX criado com sucesso!
        echo O arquivo VSIX está disponível em: %LINTER_DIR%\melodyscript-language-0.1.0.vsix
        echo Para instalar a extensão, use o comando 'code --install-extension melodyscript-language-0.1.0.vsix' ou instale manualmente pelo VSCode.
    ) else (
        echo ❌ Erro ao criar o arquivo VSIX. Verifique as mensagens de erro acima.
        exit /b 1
    )
) else (
    echo ❌ Erro ao compilar a extensão. Verifique as mensagens de erro acima.
    exit /b 1
)

exit /b 0 