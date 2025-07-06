@echo off
REM Script para executar a MelodyScript com o ambiente virtual no Windows
setlocal enabledelayedexpansion

REM Obter o diretório atual do script
set "SCRIPT_DIR=%~dp0"
set "VENV_PATH=%SCRIPT_DIR%.venv"

echo Ativando ambiente virtual em "!VENV_PATH!"

REM Verificar se o ambiente virtual existe
if not exist "!VENV_PATH!\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado em "!VENV_PATH!\Scripts\"
    echo Execute 'python -m venv .venv' para criar o ambiente virtual
    exit /b 1
)

REM Ativar o ambiente virtual
call "!VENV_PATH!\Scripts\activate.bat"

REM Verificar se funcionou
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado ou ambiente virtual nao ativado
    exit /b 1
)

echo Ambiente virtual ativado com sucesso!

REM Executar o comando MelodyScript
if "%~1"=="executar" (
    if "%~2"=="" (
        echo ERRO: Especifique o arquivo .mscr para executar
        echo Uso: %0 executar arquivo.mscr
        exit /b 1
    )
    echo Executando: python -m src.melodyscript executar "%~2"
    python -m src.melodyscript executar "%~2"
) else if "%~1"=="validar" (
    if "%~2"=="" (
        echo ERRO: Especifique o arquivo .mscr para validar
        echo Uso: %0 validar arquivo.mscr
        exit /b 1
    )
    echo Validando: python -m src.melodyscript validar "%~2"
    python -m src.melodyscript validar "%~2"
) else (
    echo Uso: %0 [executar^|validar] arquivo.mscr
    echo.
    echo Exemplos:
    echo   %0 executar examples\ola_mundo.mscr
    echo   %0 validar examples\com_erros.mscr
    exit /b 1
) 