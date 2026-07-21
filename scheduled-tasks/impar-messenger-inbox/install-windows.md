# Instalação - Tarefa Agendada Messenger Impar (Windows)

## Arquivos inclusos
- `SKILL.md` — Definição da tarefa
- `run.ps1` — Script de execução (PowerShell)
- `install-windows.md` — Estas instruções

## Pré-requisitos
- Windows 10/11
- PowerShell 5.0+ (já vem instalado)
- Claude Code CLI instalado e no PATH
- OneDrive habilitado (ou ajustar caminho em `run.ps1`)

## Instalação (máquina nova)

### 1. Criar diretórios

Abra PowerShell como **Administrador** e execute:

```powershell
$SkillDir = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora"
$LogDir = "$env:USERPROFILE\AppData\Local\Logs"

New-Item -ItemType Directory -Path $SkillDir -Force
New-Item -ItemType Directory -Path $LogDir -Force
```

### 2. Copiar arquivos

```powershell
$SkillDir = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora"

Copy-Item -Path ".\SKILL.md" -Destination "$SkillDir\"
Copy-Item -Path ".\run.ps1" -Destination "$SkillDir\"
```

### 3. Configurar permissões (importante!)

Executar no PowerShell como **Administrador**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Criar Tarefa Agendada

Opção A: **Via PowerShell (recomendado)**

Abra PowerShell como **Administrador** e execute:

```powershell
$taskName = "ImparMessengerInbox"
$taskPath = "\Claude\Scheduled-Tasks\"
$scriptPath = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora\run.ps1"

# Remover tarefa antiga se existir
Unregister-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Confirm:$false -ErrorAction SilentlyContinue

# Criar ação
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -File `"$scriptPath`""

# Criar trigger (a cada 5 minutos)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 999)

# Criar configurações da tarefa
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Registrar tarefa
Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath $taskPath `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Responder conversas não lidas do Messenger Impar a cada 5 minutos" `
    -RunLevel Highest
```

Opção B: **Via GUI do Task Scheduler**

1. Abra **Task Scheduler** (Win+R → `taskschd.msc`)
2. Clique em **Criar Pasta** → nome: `Claude`
3. Clique em **Criar Pasta** → nome: `Scheduled-Tasks` (dentro de Claude)
4. Clique direito em **Scheduled-Tasks** → **Criar Tarefa**
5. **Aba Geral:**
   - Nome: `ImparMessengerInbox`
   - Descrição: `Responder conversas não lidas do Messenger Impar`
   - ☑ Executar com privilégios mais altos
   - ☑ Executar se o usuário estiver conectado ou não
6. **Aba Acionadores:**
   - Novo → Ao iniciar
   - ☑ Habilitado
   - Novo → Agendada
   - Repetir a cada 5 minutos
7. **Aba Ações:**
   - Programa: `powershell.exe`
   - Argumentos: `-NoProfile -WindowStyle Hidden -File "C:\Users\USUARIO\.claude\scheduled-tasks\impar-messenger-inbox-hora\run.ps1"`
   - (Substituir USUARIO pelo seu nome de usuário)
8. **Aba Condições:**
   - ☑ Iniciar somente se o computador estiver conectado à rede
9. Clique **OK** e autentique quando solicitado

### 5. Verificar status

```powershell
Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

### 6. Ver logs

PowerShell:
```powershell
Get-Content "$env:USERPROFILE\AppData\Local\Logs\impar-messenger-inbox.log" -Tail 20
```

Ou abra o arquivo diretamente:
```powershell
notepad "$env:USERPROFILE\AppData\Local\Logs\impar-messenger-inbox.log"
```

## Para desativar

PowerShell como **Administrador**:
```powershell
Disable-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

Para remover completamente:
```powershell
Unregister-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\" -Confirm:$false
```

## Configuração do Caminho de Trabalho

Se estiver usando uma pasta diferente do OneDrive, edite `run.ps1` na linha 6:

```powershell
# Mude de:
$WORK_DIR = "$env:USERPROFILE\OneDrive\Kit-Piloto-Automatico-V30-DISTRIB"

# Para:
$WORK_DIR = "C:\Caminho\Ate\Sua\Pasta"
```

## Frequência

A cada 5 minutos, automaticamente (iniciando ao login ou ao iniciar o PC)

## Troubleshooting

**Tarefa não executa:**
1. Verifique se ExecutionPolicy está correto: `Get-ExecutionPolicy`
2. Teste manualmente: `powershell -NoProfile -File "C:\Users\USUARIO\.claude\scheduled-tasks\impar-messenger-inbox-hora\run.ps1"`
3. Verifique permissões: Task Scheduler → Propriedades da Tarefa → Aba "Geral" → Marque "Executar com privilégios mais altos"

**Claude CLI não encontrado:**
1. Verifique instalação: `claude --version`
2. Adicione ao PATH se necessário (procure documentação do Claude Code)

**Logs não aparecem:**
1. Verifique se pasta existe: `$env:USERPROFILE\AppData\Local\Logs`
2. Verifique permissões de escrita na pasta

