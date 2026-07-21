# 🚀 Impar Automations - Core

Este diretório contém as automações Facebook Impar para publicação automática em Marketplace e Grupos.

## 📁 Estrutura

```
impar-automations/
├── scripts/              # 23 Python scripts (gerador de fila, publicador, utilitarios)
├── data/                 # Dados e configuracao (CSVs, .env)
├── docs/                 # Documentacao completa
├── queue/                # Saida dos scripts (criado automaticamente)
├── logs/                 # Logs de execucao (criado automaticamente)
├── requirements.txt      # Dependencias Python
├── .env.template         # Template de configuracao
├── .gitignore            # Arquivo de exclusao Git
└── README.md             # Este arquivo
```

## 🔧 Instalacao

A instalacao e feita automaticamente pelo script `install-windows-auto.ps1` na raiz do repositorio:

```powershell
cd ..
.\install-windows-auto.bat
```

Isso vai:
1. Validar Python 3.10+
2. Criar venv (ambiente virtual)
3. Instalar dependencias
4. Gerar .env automaticamente
5. Validar dados (CSVs)
6. Criar diretorios necessarios

## 📝 Configuracao

### 1. Arquivo .env

O arquivo `.env` e criado automaticamente durante instalacao:

```bash
cp .env.template .env
```

Depois preencha com suas credenciais:
- `WHATSAPP_SEND_WEBHOOK_URL` - Webhook URL
- `WHATSAPP_SEND_TOKEN` - Token de autenticacao
- `OPENAI_API_KEY` - Chave API OpenAI

### 2. Dados (CSVs)

Coloque os arquivos de dados em `data/`:
- `grupos-aprovados.csv` - 96 grupos Facebook aprovados
- `imoveis-locacao.csv` - Imoveis para locacao
- `imoveis-venda.csv` - Imoveis para venda

## 🚀 Primeiros Comandos

```powershell
# Gerar fila marketplace
python scripts\generate_queue.py

# Gerar fila de grupos
python scripts\generate_group_queue.py

# Publicar em grupos (preview - pede confirmacao)
python scripts\publish_groups_playwright.py --headed

# Publicar de verdade (use com cuidado!)
python scripts\publish_groups_playwright.py --headed --publish
```

## 📚 Scripts Disponíveis

### Core Scripts (Use Frequentemente)

| Script | Funcao | Comando |
|--------|--------|---------|
| `generate_queue.py` | Gera fila marketplace | `python scripts\generate_queue.py` |
| `generate_group_queue.py` | Gera fila de grupos | `python scripts\generate_group_queue.py` |
| `publish_groups_playwright.py` | Publica em grupos | `python scripts\publish_groups_playwright.py --headed` |

### Utility Scripts

| Script | Funcao |
|--------|--------|
| `openai_enhance.py` | Melhora titulos/descricoes |
| `login-facebook.py` | Login no Facebook |
| `fetch_group_urls.py` | Descobrir novos grupos |
| `crosspost_groups_v2.py` | Publicar entre grupos |

### Debug Scripts

| Script | Funcao |
|--------|--------|
| `debug-form.py` | Debug de formulario |
| `debug-iframes.py` | Debug de iframes |
| `probe_form.py` | Investigar campos |

## 📊 Configuracoes

Editados em `.env`:

### Marketplace
- `MARKETPLACE_INTERVAL_MIN=7` - Intervalo minimo (minutos)
- `MARKETPLACE_INTERVAL_MAX=20` - Intervalo maximo (minutos)

### Grupos
- `GROUPS_INTERVAL_MINUTES=3` - Intervalo entre grupos
- `GROUPS_POSTING_HOURS=11:30,17:00,21:30` - Horarios de postagem
- `GROUPS_PER_DAY_LIMIT=30` - Limite de grupos/dia (restricao Facebook)

## ❓ Troubleshooting

| Erro | Solucao |
|------|---------|
| "ModuleNotFoundError" | `pip install -r requirements.txt` |
| "Chrome nao encontrado" | `python -m playwright install chromium` |
| "CSVs nao carregam" | Verifique encoding UTF-8 e nomes corretos |
| ".env vazio" | Preencha as credenciais em `.env` |

## 📚 Documentacao Completa

- `docs/README.md` - Overview do projeto
- `docs/MECANICO-IMPAR-PROCEDIMENTOS.md` - Procedures tecnicas
- `docs/CONFIGURAR-WEBHOOK-FACEBOOK.md` - Setup webhook
- `LEIA-PRIMEIRO.txt` - Instrucoes originais

## ✨ Pronto!

Se chegou aqui, a instalacao foi bem-sucedida. Execute os comandos da secao "Primeiros Comandos" acima.

---

**Status:** ✅ Pronto para producao  
**Ultima atualizacao:** 2026-07-21
