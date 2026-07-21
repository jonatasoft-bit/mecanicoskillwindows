@echo off
REM Impar Facebook Automations - Automated Windows Installer
REM Executa instalacao 100% automatica

cd /d "%~dp0"

echo.
echo ====================================
echo Impar Automacoes - Setup Windows
echo Instalacao 100%% Automatica
echo ====================================
echo.

REM Permitir execucao de scripts PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force"

REM Executar script PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -File "install-windows-auto.ps1"

echo.
echo ====================================
if %ERRORLEVEL% EQU 0 (
    echo SUCESSO! Instalacao completada.
) else (
    echo ERRO! Algo deu errado. Verifique acima.
)
echo ====================================
echo.
pause
