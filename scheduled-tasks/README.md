# 🔔 Automações Agendadas - Impar

Este diretório contém automações agendadas que rodam continuamente via Windows Task Scheduler.

## 📋 Automações Disponíveis

### 1. **Impar Messenger Inbox** (A cada 5 minutos)

Responde conversas não lidas do Facebook Marketplace Messenger automaticamente.

**Localização:** `impar-messenger-inbox/`

**Arquivos:**
- `SKILL.md` - Definição da tarefa e instruções
- `run.ps1` - Script de execução
- `install-windows.md` - Guia completo de instalação

**O que faz:**
- ✅ Monitora Messenger do Marketplace
- ✅ Identifica conversas não lidas (bolinha azul)
- ✅ Responde com templates automáticos
- ✅ Captura telefones de leads em CSV
- ✅ Registra logs de execução

**Como Instalar:**
```powershell
cd impar-messenger-inbox
# Siga as instruções em install-windows.md
```

**Frequência:** A cada 5 minutos (automático)

---

## 🚀 Instalação Rápida

### Pré-requisitos
- Windows 10/11
- PowerShell 5.0+ (já vem instalado)
- Claude Code CLI (https://claude.ai/code)
- OneDrive habilitado (configurável)

### Passos

```powershell
# 1. Abra PowerShell como ADMINISTRADOR

# 2. Crie diretórios
$SkillDir = "$env:USERPROFILE\.claude\scheduled-tasks\impar-messenger-inbox-hora"
New-Item -ItemType Directory -Path $SkillDir -Force

# 3. Copie arquivos (de impar-messenger-inbox/)
Copy-Item -Path ".\SKILL.md" -Destination "$SkillDir\"
Copy-Item -Path ".\run.ps1" -Destination "$SkillDir\"

# 4. Configure permissões
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 5. Crie tarefa agendada (copie comando de install-windows.md)
# ... (siga as instruções no arquivo)

# 6. Verifique
Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

---

## 📚 Documentação Completa

Veja os arquivos individuais:
- **`impar-messenger-inbox/SKILL.md`** - O que a automação faz e como funciona
- **`impar-messenger-inbox/install-windows.md`** - Instruções completas de instalação
- **`impar-messenger-inbox/run.ps1`** - Script PowerShell (não editar sem experiência)

---

## 🔍 Monitoramento

### Ver Status
```powershell
Get-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

### Ver Logs
```powershell
Get-Content "$env:USERPROFILE\AppData\Local\Logs\impar-messenger-inbox.log" -Tail 20
```

### Parar Execução
```powershell
Disable-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\"
```

### Remover Completamente
```powershell
Unregister-ScheduledTask -TaskName "ImparMessengerInbox" -TaskPath "\Claude\Scheduled-Tasks\" -Confirm:$false
```

---

## 📝 Customização

Se usar pasta diferente do OneDrive, edite `run.ps1` linha 6:

```powershell
# Mude de:
$WORK_DIR = "$env:USERPROFILE\OneDrive\Kit-Piloto-Automatico-V30-DISTRIB"

# Para seu caminho:
$WORK_DIR = "C:\Seu\Caminho\Aqui"
```

---

## ❓ Troubleshooting

| Problema | Solução |
|----------|---------|
| "Tarefa não executa" | Verifique ExecutionPolicy: `Get-ExecutionPolicy` |
| "Claude CLI não encontrado" | Instale Claude Code ou adicione ao PATH |
| "Sem permissão para criar tarefa" | Execute PowerShell como ADMINISTRADOR |
| "Logs não aparecem" | Crie pasta: `$env:USERPROFILE\AppData\Local\Logs` |

---

## 🔐 Segurança

- ✅ SKILL.md não contém credenciais reais
- ✅ Arquivo `.env` no `.gitignore`
- ✅ Logs armazenados localmente (não sincronizados)
- ✅ Tarefa roda com privilégios necessários apenas

---

**Status:** ✅ Pronto para instalação  
**Versão:** 2026-07-21  
**Frequência:** A cada 5 minutos (automático)
