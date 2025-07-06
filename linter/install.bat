@echo off
REM Script para instalar a extensão MelodyScript para VSCode no Windows

echo Instalando a extensão MelodyScript no VSCode...

REM Verificar se o VSCode está instalado
where code >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Erro: VSCode não encontrado. Por favor, instale o VSCode primeiro.
    echo Visite https://code.visualstudio.com/download para instruções de instalação.
    exit /b 1
)

REM Caminho para o arquivo VSIX (no mesmo diretório do script)
set SCRIPT_DIR=%~dp0
set VSIX_PATH=%SCRIPT_DIR%melodyscript-language-0.1.0.vsix

REM Verificar se o arquivo VSIX existe
if not exist "%VSIX_PATH%" (
    echo Erro: Arquivo VSIX não encontrado em %VSIX_PATH%
    echo Execute 'cd %SCRIPT_DIR% && npm run package' para gerar o arquivo VSIX primeiro.
    exit /b 1
)

REM Instalar a extensão
echo Instalando a extensão a partir de %VSIX_PATH%...
code --install-extension "%VSIX_PATH%"

REM Verificar se a instalação foi bem-sucedida
if %ERRORLEVEL% equ 0 (
    echo Extensão MelodyScript instalada com sucesso!
    echo Reinicie o VSCode para aplicar as alterações.
) else (
    echo Erro ao instalar a extensão. Verifique as mensagens de erro acima.
    exit /b 1
) 