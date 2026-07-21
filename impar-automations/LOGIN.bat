@echo off
REM Impar Automacoes - Login Facebook Interativo
REM Execute este arquivo para abrir navegador e fazer login

setlocal enabledelayedexpansion

echo.
echo ====================================
echo Impar Automacoes - Login Facebook
echo ====================================
echo.

REM Verificar se estamos no diretorio correto
if not exist "scripts\login-facebook.py" (
    echo ERRO: Nao estou no diretorio correto!
    echo Execute este arquivo de: impar-automations\
    pause
    exit /b 1
)

REM Verificar se venv existe
if not exist "venv\Scripts\python.exe" (
    echo ERRO: venv nao encontrado!
    echo Execute primeiro: ..\install-windows-auto.bat
    pause
    exit /b 1
)

REM Ativar venv
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Executar script de login
echo.
echo Abrindo navegador para login no Facebook...
echo Aguarde...
echo.

venv\Scripts\python.exe scripts\login-facebook.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo SUCESSO! Login realizado!
    echo ====================================
    echo.
    echo Proximos passos:
    echo   1. Gerar fila: python scripts\generate_queue.py
    echo   2. Gerar grupos: python scripts\generate_group_queue.py
    echo   3. Publicar: python scripts\publish_groups_playwright.py --headed
    echo.
) else (
    echo.
    echo ERRO! Algo deu errado.
    echo Tente novamente.
    echo.
)

pause
