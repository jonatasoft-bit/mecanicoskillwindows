# Script de verificação de automações agendadas paradas
# Execução: powershell -ExecutionPolicy Bypass -File verify-automations-status.ps1

$ErrorActionPreference = "SilentlyContinue"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "🔍 VERIFICADOR DE AUTOMAÇÕES AGENDADAS" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# 1. Verificar se rodando como Administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-Not $isAdmin) {
    Write-Host "⚠️  AVISO: Execute como Administrador para visualizar todas as tarefas" -ForegroundColor Yellow
    Write-Host "   Clique direito no PowerShell → 'Executar como administrador'" -ForegroundColor Yellow
}

# 2. Verificar Claude Code CLI
Write-Host "`n📋 1. VERIFICANDO CLAUDE CODE CLI" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

if (Get-Command claude -ErrorAction SilentlyContinue) {
    $claudeVersion = & claude --version 2>$null
    Write-Host "✅ Claude Code CLI encontrado" -ForegroundColor Green
    Write-Host "   Versão: $claudeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Claude Code CLI NÃO ENCONTRADO" -ForegroundColor Red
    Write-Host "   Ação necessária: Instale Claude Code ou adicione ao PATH" -ForegroundColor Red
}

# 3. Verificar ExecutionPolicy
Write-Host "`n📋 2. VERIFICANDO EXECUTION POLICY" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

$policy = Get-ExecutionPolicy -Scope CurrentUser
Write-Host "   Escopo CurrentUser: $policy" -ForegroundColor Yellow

if ($policy -eq "RemoteSigned" -or $policy -eq "Unrestricted") {
    Write-Host "✅ ExecutionPolicy adequada" -ForegroundColor Green
} else {
    Write-Host "❌ ExecutionPolicy restritiva ($policy)" -ForegroundColor Red
    Write-Host "   Execute no PowerShell Admin:" -ForegroundColor Yellow
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
}

# 4. Verificar Tarefas Agendadas do Claude
Write-Host "`n📋 3. VERIFICANDO TAREFAS AGENDADAS DO CLAUDE" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

$tasks = Get-ScheduledTask -TaskPath "\Claude*" -ErrorAction SilentlyContinue | Where-Object { $_.TaskPath -like "*Claude*" }

if ($tasks.Count -eq 0) {
    Write-Host "⚠️  Nenhuma tarefa encontrada em \Claude\" -ForegroundColor Yellow
} else {
    foreach ($task in $tasks) {
        $taskInfo = Get-ScheduledTaskInfo -InputObject $task
        $status = if ($task.State -eq "Ready") { "✅ Pronta" } elseif ($task.State -eq "Disabled") { "❌ Desabilitada" } else { "⚠️  $($task.State)" }

        Write-Host "`n   📌 $($task.TaskName) $status" -ForegroundColor Yellow
        Write-Host "      Caminho: $($task.TaskPath)" -ForegroundColor Gray
        Write-Host "      Estado: $($task.State)" -ForegroundColor Gray
        Write-Host "      Última execução: $($taskInfo.LastRunTime)" -ForegroundColor Gray
        Write-Host "      Última resultado: $($taskInfo.LastTaskResult)" -ForegroundColor Gray

        if ($taskInfo.LastTaskResult -ne 0) {
            Write-Host "      ⚠️  Última execução retornou erro: 0x$([Convert]::ToString($taskInfo.LastTaskResult, 16))" -ForegroundColor Red
        }
    }
}

# 5. Verificar tarefa específica - ImparMessengerInbox
Write-Host "`n📋 4. VERIFICANDO TAREFA ESPECÍFICA: IMPAR MESSENGER INBOX" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

$messengerTask = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\" -ErrorAction SilentlyContinue

if ($null -eq $messengerTask) {
    Write-Host "❌ Tarefa NÃO INSTALADA" -ForegroundColor Red
    Write-Host "`n   Para instalar, execute:" -ForegroundColor Yellow
    Write-Host "   cd $scriptPath\scheduled-tasks\impar-messenger-inbox" -ForegroundColor Cyan
    Write-Host "   .\install-windows.md (siga as instruções)" -ForegroundColor Cyan
} else {
    Write-Host "✅ Tarefa encontrada" -ForegroundColor Green

    $messengerInfo = Get-ScheduledTaskInfo -InputObject $messengerTask

    if ($messengerTask.State -eq "Ready") {
        Write-Host "   ✅ Estado: HABILITADA" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Estado: $($messengerTask.State)" -ForegroundColor Red
        Write-Host "      Para reabilitar, execute no PowerShell Admin:" -ForegroundColor Yellow
        Write-Host "      Enable-ScheduledTask -TaskName 'ImparMessengerInbox' -TaskPath '\Claude\Scheduled-Tasks\'" -ForegroundColor Cyan
    }

    Write-Host "   Última execução: $($messengerInfo.LastRunTime)" -ForegroundColor Gray
    Write-Host "   Próxima execução: $($messengerInfo.NextRunTime)" -ForegroundColor Gray

    if ($messengerInfo.LastTaskResult -ne 0 -and $messengerInfo.LastTaskResult -ne $null) {
        Write-Host "   ⚠️  Última execução retornou erro: 0x$([Convert]::ToString($messengerInfo.LastTaskResult, 16))" -ForegroundColor Red
        Write-Host "`n      Verifique os logs em:" -ForegroundColor Yellow
        Write-Host "      $env:USERPROFILE\AppData\Local\Logs\impar-messenger-inbox.log" -ForegroundColor Cyan
    }
}

# 6. Verificar arquivo SKILL.md
Write-Host "`n📋 5. VERIFICANDO ARQUIVO SKILL.MD" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

$skillPath = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora\SKILL.md"
if (Test-Path -Path $skillPath) {
    Write-Host "✅ SKILL.md encontrado" -ForegroundColor Green
    Write-Host "   Caminho: $skillPath" -ForegroundColor Gray
} else {
    Write-Host "❌ SKILL.md NÃO ENCONTRADO" -ForegroundColor Red
    Write-Host "   Caminho esperado: $skillPath" -ForegroundColor Red
    Write-Host "   Execute a instalação completa em scheduled-tasks/impar-messenger-inbox/" -ForegroundColor Yellow
}

# 7. Verificar Logs
Write-Host "`n📋 6. VERIFICANDO LOGS" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

$logPath = "$env:USERPROFILE\AppData\Local\Logs\impar-messenger-inbox.log"
if (Test-Path -Path $logPath) {
    Write-Host "✅ Log file encontrado" -ForegroundColor Green
    Write-Host "   Caminho: $logPath" -ForegroundColor Gray
    Write-Host "`n   Últimas 10 linhas:" -ForegroundColor Yellow
    Get-Content -Path $logPath -Tail 10 | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
} else {
    Write-Host "⚠️  Log file ainda não criado (esperado na primeira execução)" -ForegroundColor Yellow
    Write-Host "   Será criado em: $logPath" -ForegroundColor Gray
}

# 8. Resumo e Recomendações
Write-Host "`n📋 7. RESUMO E RECOMENDAÇÕES" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────" -ForegroundColor Magenta

Write-Host "`n🚀 SE TUDO ESTÁ VERDE (✅):" -ForegroundColor Green
Write-Host "   A automação está funcionando corretamente!" -ForegroundColor Green

Write-Host "`n🛠️  SE HÁ ITENS VERMELHOS (❌):" -ForegroundColor Red
Write-Host "   1. Verifique se Claude Code CLI está instalado" -ForegroundColor Yellow
Write-Host "   2. Verifique ExecutionPolicy com: Get-ExecutionPolicy" -ForegroundColor Yellow
Write-Host "   3. Reabilite a tarefa se desabilitada" -ForegroundColor Yellow
Write-Host "   4. Verifique os logs em AppData\Local\Logs\" -ForegroundColor Yellow
Write-Host "   5. Execute o script de instalação novamente" -ForegroundColor Yellow

Write-Host "`n📞 PARA REABILITAR UMA TAREFA DESABILITADA:" -ForegroundColor Cyan
Write-Host "   Execute no PowerShell como Administrador:" -ForegroundColor Cyan
Write-Host "   Enable-ScheduledTask -TaskName 'ImparMessengerInbox' -TaskPath '\Claude\Scheduled-Tasks\'" -ForegroundColor Cyan

Write-Host "`n📞 PARA VERIFICAR PERMISSÕES:" -ForegroundColor Cyan
Write-Host "   Get-ScheduledTask -TaskName 'ImparMessengerInbox' -TaskPath '\Claude\Scheduled-Tasks\' | Select-Object * | Format-List" -ForegroundColor Cyan

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "✅ Verificação concluída" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan
