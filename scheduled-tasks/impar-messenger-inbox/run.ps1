# Tarefa automática: Responder conversas não lidas do Messenger Impar
# Executada a cada 5 minutos via Task Scheduler

$ErrorActionPreference = "Stop"

$WORK_DIR = "$env:USERPROFILE\OneDrive\Kit-Piloto-Automatico-V30-DISTRIB"
$SKILL_FILE = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora\SKILL.md"
$LOG_DIR = "$env:USERPROFILE\AppData\Local\Logs"
$LOG_FILE = "$LOG_DIR\impar-messenger-inbox.log"

# Criar diretório de logs se não existir
if (-Not (Test-Path -Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
}

# Função de logging
function Write-Log {
    param([string]$Message)
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Add-Content -Path $LOG_FILE -Value "[$timestamp] $Message"
    Write-Host "[$timestamp] $Message"
}

Write-Log "Iniciando varredura de Messenger Impar..."

# Verificar se o SKILL.md existe
if (-Not (Test-Path -Path $SKILL_FILE)) {
    Write-Log "ERRO: SKILL.md não encontrado em $SKILL_FILE"
    exit 1
}

# Chamar Claude Code para executar a tarefa
Set-Location -Path $WORK_DIR

# Executar via Claude CLI
if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Log "Executando via Claude CLI..."
    & claude schedule run impar-messenger-inbox-hora
} else {
    Write-Log "AVISO: Claude CLI não encontrado no PATH"
}

Write-Log "Varredura concluída."
exit 0
