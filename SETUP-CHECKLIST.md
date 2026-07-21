# ✅ Setup Checklist - Impar Automações Windows

## 🎯 Pré-requisitos

- [x] Windows 10/11
- [x] Python 3.10+ instalado (https://www.python.org/downloads/)
- [x] Arquivo `install-windows-auto.bat` presente

## 📋 Fase 1: Instalação Automática

Execute em PowerShell (não precisa ser Admin):

```powershell
.\install-windows-auto.bat
```

Aguarde 2-3 minutos enquanto o script:
- Valida Python 3.10+
- Cria venv (ambiente virtual)
- Instala dependências (playwright, openai)
- Gera `.env` automaticamente
- Cria diretórios (queue, logs, temp)

Você verá ao final:
```
✅ INSTALACAO 100% COMPLETA!
```

## 📝 Fase 2: Configuração

### 2.1 - Verificar Credenciais

O script cria automaticamente `impar-automations\.env` preenchendo com:
- Variáveis de ambiente Windows (se definidas)
- Campos vazios (pode preencher manualmente)

### 2.2 - Preencher .env Manualmente (se necessário)

Abra: `impar-automations\.env`

Preencha:
```
WHATSAPP_SEND_WEBHOOK_URL=sua_url_webhook
WHATSAPP_SEND_TOKEN=seu_token
OPENAI_API_KEY=sua_chave_openai
```

## ✅ Fase 3: Verificação

Verifique que existem:
- [x] `impar-automations\venv\` (ambiente virtual)
- [x] `impar-automations\.env` (configuração)
- [x] `impar-automations\data\grupos-aprovados.csv`
- [x] `impar-automations\data\imoveis-locacao.csv`
- [x] `impar-automations\data\imoveis-venda.csv`
- [x] `impar-automations\scripts\` (23 scripts Python)

## 🚀 Fase 4: Primeiros Testes

```powershell
cd impar-automations

# Gerar fila marketplace
python scripts\generate_queue.py

# Gerar fila de grupos
python scripts\generate_group_queue.py

# Publicar em grupos (preview)
python scripts\publish_groups_playwright.py --headed
```

## ❓ Troubleshooting

| Erro | Solução |
|------|---------|
| "Python não encontrado" | Instale Python 3.10+ e marque "Add to PATH" |
| "PowerShell execution policy" | `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser` |
| "ModuleNotFoundError" | `cd impar-automations && venv\Scripts\pip.exe install -r requirements.txt` |
| "Chrome não encontrado" | `impar-automations\venv\Scripts\python.exe -m playwright install chromium` |

## ✨ Pronto!

Se chegou aqui, está tudo configurado. Comece pelos testes da Fase 4 acima.
