@echo off
REM Impar Automations - Iniciar Dashboard
REM Abre o dashboard visual em http://localhost:5000

echo.
echo ====================================
echo Impar Automations - Dashboard
echo ====================================
echo.

REM Verificar se estamos no diretorio correto
if not exist "scripts\web_server.py" (
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

REM Instalar dependencias se necessario
echo.
echo Verificando dependencias...
venv\Scripts\python.exe -m pip install flask -q

REM Iniciar dashboard
echo.
echo Iniciando dashboard...
echo Navegador abrira em alguns segundos em: http://localhost:5000
echo.
echo Para parar o servidor: Pressione Ctrl+C
echo.

venv\Scripts\python.exe scripts\web_server.py

pause
