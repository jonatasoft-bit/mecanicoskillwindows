# 🖥️ Impar Automações Facebook - Setup Automático Windows

Automação completa para publicação em Marketplace e Grupos Facebook com **instalação 100% automática em UM COMANDO**.

## 🚀 Quick Start (30 segundos)

```powershell
.\install-windows-auto.bat
```

**Isso faz tudo automaticamente:**
- ✅ Valida Python 3.10+
- ✅ Cria ambiente virtual (venv)
- ✅ Instala dependências
- ✅ Gera `.env` automaticamente
- ✅ Cria diretórios necessários

Tempo: 2-3 minutos | Resultado: Tudo pronto! ✨

---

## 📋 Pré-requisitos

- **Windows 10/11**
- **Python 3.10+** ([baixar](https://www.python.org/downloads/))
  - ⚠️ Marque "Add Python to PATH" durante instalação
- Este repositório clonado

---

## 📁 O Que Está Incluído

```
mecanicoskillwindows/
├── install-windows-auto.bat    ⭐ Clique aqui para instalar
├── install-windows-auto.ps1    (script PowerShell automático)
├── SETUP-CHECKLIST.md          (checklist pós-instalação)
├── README.md                   (este arquivo)
└── impar-automations/          (ZIP extraído)
    ├── scripts/                (23 Python scripts)
    ├── data/                   (CSVs + configuração)
    ├── docs/                   (documentação)
    ├── requirements.txt
    └── .env.template
```

---

## 🔧 Como Usar

### 1. Clonar Repositório
```bash
git clone https://github.com/jonatasoft-bit/mecanicoskillwindows.git
cd mecanicoskillwindows
```

### 2. Executar Instalador
```powershell
.\install-windows-auto.bat
```

### 3. Verificar Instalação
Veja: `SETUP-CHECKLIST.md`

### 4. Primeiros Comandos
```powershell
cd impar-automations

# Gerar fila marketplace
python scripts\generate_queue.py

# Gerar fila de grupos (96 grupos)
python scripts\generate_group_queue.py

# Publicar em grupos (preview antes de publicar de verdade)
python scripts\publish_groups_playwright.py --headed
```

---

## 📊 O Que o Script Faz

| Etapa | Ação |
|-------|------|
| 1/7 | Valida Python 3.10+ |
| 2/7 | Cria venv (ambiente virtual) |
| 3/7 | Ativa venv |
| 4/7 | Instala dependências (playwright, openai) |
| 5/7 | Gera `.env` automaticamente |
| 6/7 | Valida CSVs e cria diretórios |
| 7/7 | Exibe resumo e próximos passos |

---

## 🔐 Credenciais (Automáticas)

O script cria `impar-automations\.env` automaticamente:

### Opção 1: Via Variáveis de Ambiente Windows
```powershell
$env:WHATSAPP_SEND_WEBHOOK_URL = "https://..."
$env:WHATSAPP_SEND_TOKEN = "seu_token"
$env:OPENAI_API_KEY = "sk-..."
```

Após definir, execute o instalador. O `.env` será preenchido automaticamente.

### Opção 2: Preencher Manualmente
Se não tiver variáveis de ambiente, o script cria um `.env` vazio. Abra e preencha os campos necessários.

---

## 📚 Arquivos Importantes

- **`install-windows-auto.ps1`** - Script PowerShell (automático)
- **`install-windows-auto.bat`** - Wrapper batch (execute isto)
- **`SETUP-CHECKLIST.md`** - Checklist pós-instalação
- **`impar-automations/docs/README.md`** - Documentação detalhada
- **`impar-automations/docs/MECANICO-IMPAR-PROCEDIMENTOS.md`** - Procedures técnicas

---

## ❓ Troubleshooting

### "Python não encontrado"
```
Solução: Instale Python 3.10+ de https://www.python.org/downloads/
         IMPORTANTE: Marque "Add Python to PATH"
```

### "PowerShell execution policy"
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
```

### "Chrome/Chromium não encontrado"
```powershell
cd impar-automations
venv\Scripts\python.exe -m playwright install chromium
```

### "ModuleNotFoundError"
```powershell
cd impar-automations
venv\Scripts\pip.exe install -r requirements.txt
```

---

## 🎯 Scripts Disponíveis

| Script | Função | Uso |
|--------|--------|-----|
| `generate_queue.py` | Gera fila marketplace | `python scripts\generate_queue.py` |
| `generate_group_queue.py` | Gera fila de 96 grupos | `python scripts\generate_group_queue.py` |
| `publish_groups_playwright.py` | Publica em grupos | `python scripts\publish_groups_playwright.py --headed` |
| `openai_enhance.py` | Melhora títulos/descrições | `python scripts\openai_enhance.py` |
| Mais 19 scripts | Utilitários, debug, etc | Veja em `scripts/` |

---

## ✨ Resultado Esperado

**Antes:** 5 passos manuais + risco de erros + configuração manual  
**Depois:** 1 comando + tudo automático + 2-3 minutos

---

## 📞 Suporte

Verifique a documentação em:
- `SETUP-CHECKLIST.md` - Checklist e troubleshooting rápido
- `impar-automations/docs/MECANICO-IMPAR-PROCEDIMENTOS.md` - Procedures completas
- `impar-automations/LEIA-PRIMEIRO.txt` - Instruções originais

---

**Versão:** 2026-07-21  
**Plataforma:** Windows (PowerShell + Batch)  
**Status:** ✅ Pronto para produção
