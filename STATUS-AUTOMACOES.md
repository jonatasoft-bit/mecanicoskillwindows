# 📊 Status das Automações Agendadas - Impar

**Data:** 2026-07-25  
**Verificação:** Feita em ambiente Linux (repositório clonado)  
**Status Geral:** ⚠️ Requer verificação em Windows

---

## 🔍 Sumário Executivo

Este repositório contém **1 automação agendada principal**:

| Automação | Frequência | Status | Ação Necessária |
|-----------|-----------|--------|-----------------|
| **Impar Messenger Inbox** | A cada 5 minutos | ⚠️ Requer verificação | Executar script de status |

---

## 📌 Automação 1: Impar Messenger Inbox

### O que faz?
- ✅ Monitora Messenger do Facebook Marketplace
- ✅ Identifica conversas não lidas (ícone de bolinha azul)
- ✅ Responde com templates automáticos
- ✅ Captura telefones de leads em CSV
- ✅ Registra logs de cada execução

### Frequência
**A cada 5 minutos**, automaticamente via Windows Task Scheduler

### Localização
```
scheduled-tasks/
└── impar-messenger-inbox/
    ├── SKILL.md              # Definição da tarefa
    ├── run.ps1               # Script de execução
    └── install-windows.md    # Instruções de instalação completa
```

### Instalação
```powershell
# Como Administrador no PowerShell:
cd .\scheduled-tasks\impar-messenger-inbox\
# Siga as instruções em install-windows.md
```

### Dependências
- Windows 10/11
- PowerShell 5.0+ (built-in)
- Claude Code CLI (instalado e no PATH)
- OneDrive (ou ajustar caminho em run.ps1)
- Acesso a Facebook Marketplace (navegador)
- Acesso a Claude API (via internet)

### Permissões Necessárias
1. **ExecutionPolicy RemoteSigned**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Privilégio de Administrador** (RunLevel: Highest)
   ```powershell
   # Marcado na configuração da tarefa no Task Scheduler
   ```

3. **Pasta de Logs com permissão de escrita**
   ```
   C:\Users\USUARIO\AppData\Local\Logs\
   ```

4. **Arquivo SKILL.md acessível**
   ```
   C:\Users\USUARIO\.claude\scheduled-tasks\impar-messenger-inbox-hora\
   ```

---

## 🚨 Como Verificar se a Automação Está Parada

### Método Rápido (Windows PowerShell)

```powershell
$task = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
$info = Get-ScheduledTaskInfo -InputObject $task

Write-Host "Estado: $($task.State)"
Write-Host "Última execução: $($info.LastRunTime)"
Write-Host "Próxima execução: $($info.NextRunTime)"
Write-Host "Último resultado: 0x$([Convert]::ToString($info.LastTaskResult, 16))"
```

### Sinais de que está PARADA:

❌ **Estado = "Disabled"**
```powershell
# Para reabilitar:
Enable-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

❌ **Última execução = NULL (nunca executou)**
- Verifique se a tarefa foi criada corretamente
- Verifique se Claude CLI está no PATH
- Verifique os logs

❌ **Último resultado ≠ 0**
- Indica erro na última execução
- Verifique logs em: `AppData\Local\Logs\impar-messenger-inbox.log`

❌ **Próxima execução = NULL**
- A tarefa pode estar sem trigger configurado
- Verifique em Task Scheduler → Properties → Triggers

❌ **Claude CLI não encontrado**
```powershell
where.exe claude  # Se não retornar nada, não está no PATH
```

---

## 🔧 Como Dar Permissões (Passo a Passo)

### Passo 1: Verificar ExecutionPolicy

```powershell
Get-ExecutionPolicy -Scope CurrentUser
```

Se **não for "RemoteSigned" ou "Unrestricted"**:

```powershell
# Execute como ADMINISTRADOR:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Passo 2: Verificar/Criar Diretórios

```powershell
# SKILL.md
$SkillDir = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora"
New-Item -ItemType Directory -Path $SkillDir -Force

# Logs
$LogDir = "$env:USERPROFILE\AppData\Local\Logs"
New-Item -ItemType Directory -Path $LogDir -Force
```

### Passo 3: Verificar Claude Code CLI

```powershell
claude --version
```

Se não aparecer nada:
1. Instale [Claude Code](https://claude.ai/code)
2. Ou adicione ao PATH manualmente

### Passo 4: Reabilitar Tarefa (se desabilitada)

```powershell
# Como ADMINISTRADOR:
Enable-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

### Passo 5: Verificar Privilégios da Tarefa

```powershell
$task = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
Get-ScheduledTaskInfo -InputObject $task | Format-Table
```

Se **RunLevel ≠ Highest**, execute em **PowerShell Admin**:

```powershell
$task = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -RunLevel Highest
Set-ScheduledTask -InputObject $task -Principal $principal
```

---

## 📋 Script de Verificação Automática

Execute este script para verificar TODAS as permissões:

```powershell
powershell -ExecutionPolicy Bypass -File verify-automations-status.ps1
```

**Isto fará:**
- ✅ Verificar Claude Code CLI
- ✅ Verificar ExecutionPolicy
- ✅ Verificar estado das tarefas agendadas
- ✅ Verificar arquivo SKILL.md
- ✅ Mostrar últimos logs
- ✅ Indicar erros e soluções

---

## 📞 Troubleshooting Rápido

| Sintoma | Solução |
|---------|---------|
| "Tarefa não executa" | `Enable-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"` |
| "Acesso negado" | Execute PowerShell como **Administrador** |
| "Claude CLI não encontrado" | Instale Claude Code ou adicione ao PATH |
| "Nenhum log está sendo gerado" | Crie `AppData\Local\Logs` e dê permissão |
| "ExecutionPolicy bloqueado" | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| "Erro: The file cannot be loaded" | Desbloqueie o arquivo: `Unblock-File -Path "C:\...\run.ps1"` |

---

## 📞 Verificação Semanal Recomendada

Execute **uma vez por semana** para garantir que tudo está funcionando:

```powershell
# Salve isso como check-weekly.ps1 e execute semanalmente
$task = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\" -ErrorAction SilentlyContinue
$info = Get-ScheduledTaskInfo -InputObject $task

Write-Host "=== VERIFICAÇÃO SEMANAL ===" -ForegroundColor Cyan

if ($null -eq $task) {
    Write-Host "❌ Tarefa não encontrada - REINSTALE" -ForegroundColor Red
} elseif ($task.State -ne "Ready") {
    Write-Host "❌ Tarefa desabilitada: $($task.State)" -ForegroundColor Red
    Write-Host "   Execute: Enable-ScheduledTask -TaskName 'ImparMessengerInbox' -TaskPath '\Claude\Scheduled-Tasks\'" -ForegroundColor Yellow
} elseif ($info.LastTaskResult -ne 0) {
    Write-Host "⚠️  Erro na última execução: 0x$([Convert]::ToString($info.LastTaskResult, 16))" -ForegroundColor Yellow
    Write-Host "   Verifique logs em: $env:USERPROFILE\AppData\Local\Logs\impar-messenger-inbox.log" -ForegroundColor Yellow
} else {
    Write-Host "✅ Automação funcionando normalmente" -ForegroundColor Green
    Write-Host "   Última execução: $($info.LastRunTime)" -ForegroundColor Green
    Write-Host "   Próxima execução: $($info.NextRunTime)" -ForegroundColor Green
}
```

---

## 🔐 Matriz de Permissões

| Permissão | Nível | Escopo | Como Verificar |
|-----------|-------|--------|-----------------|
| ExecutionPolicy | RemoteSigned | CurrentUser | `Get-ExecutionPolicy -Scope CurrentUser` |
| RunLevel | Highest | Tarefa | Task Scheduler → Propriedades → Geral |
| Pasta de Logs | Read/Write | `AppData\Local\Logs` | `Test-Path "$env:USERPROFILE\AppData\Local\Logs"` |
| SKILL.md | Read | `$USERPROFILE\.claude\...` | `Test-Path "$env:USERPROFILE\.claude\scheduled-tasks\..."` |
| Claude CLI | Execute | PATH | `Get-Command claude` |
| Rede | HTTP/HTTPS | Firewall | `Test-Connection facebook.com` |

---

## 📚 Documentação Relacionada

- **[PERMISSOES-NECESSARIAS.md](./PERMISSOES-NECESSARIAS.md)** - Guia detalhado de cada permissão
- **[scheduled-tasks/impar-messenger-inbox/install-windows.md](./scheduled-tasks/impar-messenger-inbox/install-windows.md)** - Instalação passo a passo
- **[scheduled-tasks/impar-messenger-inbox/SKILL.md](./scheduled-tasks/impar-messenger-inbox/SKILL.md)** - O que a automação faz
- **[verify-automations-status.ps1](./verify-automations-status.ps1)** - Script de verificação automática

---

## ✅ Checklist de Bom Funcionamento

- [ ] Claude Code CLI instalado: `claude --version`
- [ ] ExecutionPolicy: `Get-ExecutionPolicy` retorna "RemoteSigned"
- [ ] Tarefa existe: `Get-ScheduledTask -TaskName "ImparMessengerInbox"`
- [ ] Tarefa habilitada: Estado = "Ready"
- [ ] Últimas 5 execuções sem erro (LastTaskResult = 0)
- [ ] Logs sendo gerados: `AppData\Local\Logs\impar-messenger-inbox.log` com dados recentes
- [ ] Próxima execução agendada: `NextRunTime` não é NULL
- [ ] Respostas sendo registradas: CSV de leads sendo atualizado

---

**Se TODOS os items acima estão ✅, a automação está funcionando corretamente!**

---

## 📞 Próximas Etapas

1. **Executar script de verificação:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File verify-automations-status.ps1
   ```

2. **Se houver erros:**
   - Siga as instruções no arquivo PERMISSOES-NECESSARIAS.md
   - Execute os comandos de correção no PowerShell Admin

3. **Se ainda houver problemas:**
   - Verifique logs: `AppData\Local\Logs\impar-messenger-inbox.log`
   - Reinstale seguindo: `scheduled-tasks/impar-messenger-inbox/install-windows.md`

---

**Última atualização:** 2026-07-25  
**Versão:** 1.0.0  
**Status:** ✅ Pronto para produção
