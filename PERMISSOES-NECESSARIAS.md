# 🔐 Permissões Necessárias para Automações Agendadas

Este documento descreve as permissões necessárias para que as automações agendadas funcionem corretamente.

## 📋 Checklist de Permissões

### 1. ✅ ExecutionPolicy (PowerShell)

**O que é:** Controla quais scripts PowerShell podem ser executados.

**Status atual:** Execute para verificar:
```powershell
Get-ExecutionPolicy -Scope CurrentUser
```

**Permissão necessária:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Interpretação:**
- `RemoteSigned` = Scripts locais podem rodar; scripts baixados precisam de assinatura
- `Unrestricted` = Todos os scripts podem rodar (menos seguro)

**Quem precisa:** O usuário que está executando a automação

---

### 2. ✅ Privilégios do Task Scheduler

**O que é:** A tarefa agendada precisa de permissões elevadas (Admin) para interagir com o navegador.

**Como verificar:**
```powershell
Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\" | Select-Object -Property TaskName, RunLevel
```

**Permissão necessária:**

A tarefa deve estar com `RunLevel = Highest`:

```powershell
# No PowerShell como ADMINISTRADOR:
$task = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -RunLevel Highest
Set-ScheduledTask -InputObject $task -Principal $principal
```

**Ou via GUI Task Scheduler:**
1. Abra `taskschd.msc`
2. Navegue até `\Claude\Scheduled-Tasks\ImparMessengerInbox`
3. Clique direito → Propriedades
4. Aba "Geral" → Marque "Executar com privilégios mais altos"
5. Clique OK e autentique

---

### 3. ✅ Permissões de Pasta (Logs)

**O que é:** A pasta de logs precisa de permissão de escrita.

**Caminho:** `C:\Users\USUARIO\AppData\Local\Logs`

**Como criar/verificar:**
```powershell
$logDir = "$env:USERPROFILE\AppData\Local\Logs"
if (-Not (Test-Path -Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force
}
```

**Permissão necessária:** Seu usuário deve ter permissão de escrita

**Como verificar:**
```powershell
# Teste escrevendo um arquivo
Add-Content -Path "$env:USERPROFILE\AppData\Local\Logs\test.log" -Value "teste" -ErrorAction Stop
Remove-Item -Path "$env:USERPROFILE\AppData\Local\Logs\test.log" -Force
Write-Host "✅ Permissão de escrita OK"
```

---

### 4. ✅ Permissões de Arquivo SKILL.md

**O que é:** O arquivo que define a automação precisa estar acessível.

**Caminho:** `C:\Users\USUARIO\.claude\scheduled-tasks\impar-messenger-inbox-hora\SKILL.md`

**Como verificar:**
```powershell
$skillFile = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora\SKILL.md"
if (Test-Path -Path $skillFile) {
    Write-Host "✅ SKILL.md acessível"
    Get-Item -Path $skillFile | Select-Object LastWriteTime, Length
} else {
    Write-Host "❌ SKILL.md não encontrado"
}
```

**Permissão necessária:** Leitura do arquivo

---

### 5. ✅ Acesso ao Claude Code CLI

**O que é:** A automação precisa chamar o comando `claude` para executar a tarefa.

**Como verificar:**
```powershell
claude --version
```

**Se não encontrar:**

1. **Verifique se está instalado:**
   ```powershell
   where.exe claude
   ```

2. **Adicione ao PATH (se necessário):**
   - Windows 10/11: Configurações → Sistema → Variáveis de ambiente
   - Encontre `Path` em "Variáveis de ambiente do usuário"
   - Clique "Editar"
   - Adicione o caminho onde Claude Code está instalado
   - Exemplo: `C:\Users\USUARIO\AppData\Local\Programs\Claude`
   - Reinicie o PowerShell após modificar

**Permissão necessária:** Acesso ao executável

---

### 6. ✅ Conectividade de Rede

**O que é:** A automação precisa acessar Facebook Marketplace e Claude API.

**Como verificar:**
```powershell
# Teste conexão com Facebook
Test-Connection -ComputerName facebook.com -Count 1

# Teste conexão com Claude API
Invoke-WebRequest -Uri "https://api.anthropic.com/healthz" -UseBasicParsing | Select-Object StatusCode
```

**Permissão necessária:** Acesso HTTP/HTTPS desbloqueado pelo firewall

**Se bloquear:**
- Firewall do Windows (Defender)
- Antivírus corporativo
- Proxy corporativo
- VPN

---

### 7. ✅ Permissão de Iniciar Navegador

**O que é:** A automação abre o navegador via Playwright/Selenium.

**Como verificar:**
```powershell
# Teste se Playwright está instalado
python -m pip list | grep -i playwright
```

**Permissão necessária:**
- Windows: Nenhuma especial (aplicativos podem iniciar navegadores)
- Corporativo: Pode ser bloqueado por políticas de segurança

---

## 🔧 Script de Verificação Automática

Execute para verificar TODAS as permissões:

```powershell
powershell -ExecutionPolicy Bypass -File verify-automations-status.ps1
```

**Isto verificará:**
- ✅ Claude Code CLI instalado
- ✅ ExecutionPolicy adequada
- ✅ Tarefas agendadas ativas
- ✅ Arquivo SKILL.md acessível
- ✅ Logs sendo gerados
- ✅ Erros nas últimas execuções

---

## 🚀 Passo a Passo: Dar Permissões Completas

### Para um novo setup:

```powershell
# 1. Execute PowerShell como ADMINISTRADOR

# 2. Configure ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Crie os diretórios
$SkillDir = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora"
$LogDir = "$env:USERPROFILE\AppData\Local\Logs"
New-Item -ItemType Directory -Path $SkillDir -Force
New-Item -ItemType Directory -Path $LogDir -Force

# 4. Copie os arquivos (do repositório)
$RepoDir = "C:\Users\USUARIO\CAMINHO_DO_REPO"
Copy-Item -Path "$RepoDir\scheduled-tasks\impar-messenger-inbox\*" -Destination "$SkillDir\" -Force

# 5. Configure a tarefa (veja install-windows.md para comando completo)
# [Execute o comando em install-windows.md seção 4 - Criar Tarefa Agendada]

# 6. Verifique
Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

---

## 🛠️ Troubleshooting de Permissões

| Erro | Solução |
|------|---------|
| "Cannot be loaded because running scripts is disabled" | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| "Access denied" ao criar tarefa | Execute PowerShell como **Administrador** |
| "Tarefa não executa" | Marque "Executar com privilégios mais altos" |
| "Claude CLI não encontrado" | Instale Claude Code ou adicione ao PATH |
| "Permissão negada ao escrever logs" | Crie pasta `AppData\Local\Logs` e dê permissão |
| "Firewall bloqueia execução" | Configure exceções no Windows Defender Firewall |
| "Proxy corporativo bloqueia" | Configure proxy em `~\.claude\settings.json` |

---

## 📞 Verificação Rápida

Executar **uma vez a cada semana** para garantir que tudo está funcionando:

```powershell
# Script rápido (30 segundos)
$task = Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\" -ErrorAction SilentlyContinue
$info = Get-ScheduledTaskInfo -InputObject $task

if ($task.State -eq "Ready" -and $info.LastTaskResult -eq 0) {
    Write-Host "✅ Automação funcionando corretamente"
} else {
    Write-Host "⚠️ Problema detectado - execute verify-automations-status.ps1"
}
```

---

## 📚 Referências Adicionais

- [Microsoft: Set-ExecutionPolicy](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)
- [Microsoft: Register-ScheduledTask](https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/register-scheduledtask)
- [Microsoft: Windows Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)
- [Claude Code: Documentation](https://claude.ai/code)

---

**Última atualização:** 2026-07-25  
**Status:** ✅ Pronto para produção
