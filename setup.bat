@echo off
REM Script para configuração do ambiente de desenvolvimento da MelodyScript no Windows

echo Configurando ambiente de desenvolvimento para MelodyScript...

REM Verificar se o Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erro: Python nao encontrado. Por favor, instale o Python 3.
    exit /b 1
)

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv .venv

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar dependências
echo Instalando dependencias...
pip install -r requirements.txt

echo Ambiente de desenvolvimento configurado com sucesso!
echo Para ativar o ambiente virtual, execute:
echo .venv\Scripts\activate.bat

echo Para executar o exemplo 'Ola Mundo', ative o ambiente virtual e digite:
echo python src/melodyscript.py executar examples/ola_mundo.mscr

pause 