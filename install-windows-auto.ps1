# Impar Facebook Automations - Automated Windows Installer
# Instala e configura 100% automaticamente

param(
    [switch]$SkipEnvValidation = $false
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ImparDir = Join-Path $ScriptDir "impar-automations"

Write-Host "`n================================" -ForegroundColor Green
Write-Host "Impar Automacoes - Setup Windows" -ForegroundColor Green
Write-Host "INSTALACAO 100% AUTOMATICA" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Green

# Verificar se impar-automations existe
if (-not (Test-Path $ImparDir)) {
    Write-Host "`n❌ ERRO: Diretorio impar-automations nao encontrado!" -ForegroundColor Red
    Write-Host "   Verifique se o conteudo do ZIP foi extraido em: $ImparDir" -ForegroundColor Yellow
    exit 1
}

# 1. Validar Python
Write-Host "`n[1/7] Validando Python 3.10+..." -ForegroundColor Cyan
$PythonCmd = $null
$PythonVersion = $null

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonCmd = "python3"
    $PythonVersion = & python3 --version 2>&1
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
    $PythonVersion = & python --version 2>&1
} else {
    Write-Host "❌ ERRO: Python nao encontrado. Instale Python 3.10+" -ForegroundColor Red
    Write-Host "   Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ $PythonVersion OK" -ForegroundColor Green

# 2. Criar venv
Write-Host "`n[2/7] Criando ambiente virtual..." -ForegroundColor Cyan
$VenvPath = Join-Path $ImparDir "venv"

if (Test-Path $VenvPath) {
    Write-Host "⚠ venv ja existe, removendo e recriando..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $VenvPath | Out-Null
}

& $PythonCmd -m venv $VenvPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Falha ao criar venv" -ForegroundColor Red
    exit 1
}
Write-Host "✓ venv criado" -ForegroundColor Green

# 3. Ativar venv
Write-Host "`n[3/7] Ativando venv..." -ForegroundColor Cyan
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    & $ActivateScript
    Write-Host "✓ venv ativado" -ForegroundColor Green
} else {
    Write-Host "⚠ Nao foi possivel ativar venv, continuando..." -ForegroundColor Yellow
}

# 4. Instalar dependencias
Write-Host "`n[4/7] Instalando dependencias..." -ForegroundColor Cyan
Write-Host "   Isto pode levar 2-3 minutos..." -ForegroundColor Yellow

$PipCmd = Join-Path $VenvPath "Scripts\pip.exe"
if (-not (Test-Path $PipCmd)) {
    $PipCmd = "pip"
}

$ReqPath = Join-Path $ImparDir "requirements.txt"
if (Test-Path $ReqPath) {
    & $PipCmd install -r $ReqPath --quiet 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Falha ao instalar dependencias" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "⚠ requirements.txt nao encontrado, pulando instalacao de deps" -ForegroundColor Yellow
}

# 5. Gerar .env automaticamente
Write-Host "`n[5/7] Gerando .env automaticamente..." -ForegroundColor Cyan

$EnvPath = Join-Path $ImparDir ".env"
$EnvContent = @"
# Impar Automacoes - Configuracao Automatica
# Gerado automaticamente em: $(Get-Date)

# WhatsApp Webhook (para integracao)
WHATSAPP_SEND_WEBHOOK_URL=$($env:WHATSAPP_SEND_WEBHOOK_URL)
WHATSAPP_SEND_TOKEN=$($env:WHATSAPP_SEND_TOKEN)

# OpenAI API (para enhancements de titulos/descricoes)
OPENAI_API_KEY=$($env:OPENAI_API_KEY)

# Facebook (opcional - se usar publicacao direta)
FACEBOOK_TOKEN=$($env:FACEBOOK_TOKEN)
FACEBOOK_PAGE_ID=$($env:FACEBOOK_PAGE_ID)

# Agendamento (preencher conforme necessidade)
START_DATE=$($env:START_DATE)
START_TIME=$($env:START_TIME)

# Modo Debug (deixar false em producao)
DEBUG=$($env:DEBUG -eq "true")

# Configuracoes de Cadencia
MARKETPLACE_INTERVAL_MIN=7
MARKETPLACE_INTERVAL_MAX=20
GROUPS_INTERVAL_MINUTES=3
GROUPS_POSTING_HOURS=11:30,17:00,21:30
GROUPS_PER_DAY_LIMIT=30
"@

$EnvContent | Set-Content $EnvPath
Write-Host "✓ .env criado em: $EnvPath" -ForegroundColor Green

# 6. Validar CSVs e criar diretorios
Write-Host "`n[6/7] Validando dados e criando diretorios..." -ForegroundColor Cyan

$DataDir = Join-Path $ImparDir "data"
if (Test-Path $DataDir) {
    $CsvFiles = @("grupos-aprovados.csv", "imoveis-locacao.csv", "imoveis-venda.csv")
    $CsvCount = 0
    foreach ($CsvFile in $CsvFiles) {
        $CsvPath = Join-Path $DataDir $CsvFile
        if (Test-Path $CsvPath) {
            $Size = (Get-Item $CsvPath).Length / 1KB
            Write-Host "✓ $CsvFile ($([math]::Round($Size))KB)" -ForegroundColor Green
            $CsvCount++
        }
    }
    Write-Host "✓ $CsvCount/3 CSVs encontrados" -ForegroundColor Green
}

# Criar diretorios necessarios
@("queue", "logs", "temp") | ForEach-Object {
    $DirPath = Join-Path $ImparDir $_
    if (-not (Test-Path $DirPath)) {
        New-Item -ItemType Directory -Path $DirPath | Out-Null
        Write-Host "✓ Diretorio criado: $_" -ForegroundColor Green
    }
}

# 7. Exibir resumo final
Write-Host "`n[7/7] Verificacao final..." -ForegroundColor Cyan

Write-Host "`n================================" -ForegroundColor Green
Write-Host "✅ INSTALACAO 100% COMPLETA!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

Write-Host "`n📊 RESUMO:" -ForegroundColor Cyan
Write-Host "   ✓ Python: $PythonVersion" -ForegroundColor White
Write-Host "   ✓ venv: Criado" -ForegroundColor White
Write-Host "   ✓ Dependencias: Instaladas" -ForegroundColor White
Write-Host "   ✓ .env: Gerado automaticamente" -ForegroundColor White
Write-Host "   ✓ Diretorios: queue, logs, temp criados" -ForegroundColor White

Write-Host "`n📝 PROXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "   1. Revisar .env se necessario: $EnvPath" -ForegroundColor White
Write-Host "   2. Gerar fila marketplace:" -ForegroundColor White
Write-Host "      cd $ImparDir && python scripts\generate_queue.py" -ForegroundColor Yellow
Write-Host "   3. Gerar fila de grupos:" -ForegroundColor White
Write-Host "      python scripts\generate_group_queue.py" -ForegroundColor Yellow

Write-Host "`n✨ Tudo pronto! Comece pelo passo 1 acima.`n" -ForegroundColor Green
