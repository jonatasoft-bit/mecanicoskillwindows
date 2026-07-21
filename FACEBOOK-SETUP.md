# 🔌 Conectar Facebook - Guia Completo

Como conectar suas automações ao Facebook Marketplace e começar a publicar.

## 📋 Pré-requisitos

✅ Instalação completa rodada (`.\install-windows-auto.bat`)  
✅ Python venv ativado  
✅ Dependências instaladas  
✅ Conta Facebook com acesso ao Marketplace

---

## 🚀 Step-by-Step: Conectando ao Facebook

### PASSO 1: Login no Facebook (Autenticação)

Este script abre o navegador e você faz login manualmente:

```powershell
cd impar-automations
python scripts\login-facebook.py
```

**O que acontece:**
1. ✅ Abre navegador com Facebook Marketplace
2. ✅ Você digita email/senha (é você quem faz login)
3. ✅ Confirma 2FA se solicitado
4. ✅ Script captura cookies de autenticação
5. ✅ Salva em `.cookies.json` (automático)

**Resultado:** Arquivo `.cookies.json` criado ✓

---

### PASSO 2: Gerar Fila de Publicação

Prepara os anúncios para serem publicados:

```powershell
python scripts\generate_queue.py
```

**O que faz:**
- ✅ Lê CSV de imóveis (locação + venda)
- ✅ Cria fila de publicação
- ✅ Define cadência (7-20 minutos automática)
- ✅ Salva em `queue/marketplace_queue_*.csv`

**Resultado:** Arquivo de fila criado ✓

---

### PASSO 3: Gerar Fila de Grupos (96 Grupos)

Prepara publicação nos 96 grupos:

```powershell
python scripts\generate_group_queue.py
```

**O que faz:**
- ✅ Lê grupos aprovados (grupos-aprovados.csv)
- ✅ Distribui imóveis entre grupos
- ✅ Define horários (11:30, 17:00, 21:30)
- ✅ Respeita limite Facebook (30 grupos/dia)
- ✅ Salva em `queue/groups_queue_*.csv`

**Resultado:** Fila de grupos criada ✓

---

### PASSO 4 (Opcional): Melhorar com IA

Usa OpenAI para melhorar títulos e descrições:

```powershell
python scripts\openai_enhance.py
```

**Pré-requisito:**
- Ter `OPENAI_API_KEY` configurada no `.env`

**O que faz:**
- ✅ Lê descrições dos imóveis
- ✅ Usa GPT para melhorar títulos
- ✅ Aprimora descrições
- ✅ Salva em `queue/enhanced_listings.csv`

**Como configurar:**
1. Abra `.env`
2. Adicione: `OPENAI_API_KEY=sk-seu-api-key`
3. (Pegue a chave em: https://platform.openai.com/api-keys)

---

### PASSO 5: Publicar nos Grupos

#### Modo Preview (Recomendado primeiro)
Visualiza antes de publicar:

```powershell
python scripts\publish_groups_playwright.py --headed
```

- ✅ Abre navegador (você vê tudo)
- ✅ Simula publicação
- ✅ Não publica de verdade
- ✅ Ideal para testar

#### Modo Produção (Publicar de Verdade)
Após validar no preview, publique para real:

```powershell
python scripts\publish_groups_playwright.py --headed --publish
```

- ✅ Publica nos grupos automaticamente
- ✅ Respeita limite de 30 grupos/dia
- ✅ Logs registram tudo

#### Opções Avançadas
```powershell
# Publicar em 10 grupos
python scripts\publish_groups_playwright.py --headed --groups 10

# Modo sem navegador (headless)
python scripts\publish_groups_playwright.py --publish

# Combinar opções
python scripts\publish_groups_playwright.py --headed --publish --groups 20
```

---

## 📊 Fluxo Completo (Primeira Vez)

```powershell
cd impar-automations

# 1. Conectar ao Facebook (fazer login)
python scripts\login-facebook.py
# → Abre navegador, você faz login, salva .cookies.json

# 2. Gerar filas
python scripts\generate_queue.py
python scripts\generate_group_queue.py

# 3. Melhorar (opcional)
python scripts\openai_enhance.py

# 4. Visualizar antes de publicar
python scripts\publish_groups_playwright.py --headed

# 5. Se tudo OK, publicar para real
python scripts\publish_groups_playwright.py --headed --publish
```

**Tempo total:** ~10-15 minutos

---

## 🔐 Segurança

### Cookies (.cookies.json)
- ⚠️ Contém tokens de autenticação
- 🚫 **NUNCA commite em repositório público**
- 📁 Já está em `.gitignore` (protegido)
- 💾 Guarde seguro no seu computador

### .env
- ⚠️ Contém credenciais sensíveis
- 🚫 **NUNCA commite**
- 📁 Já está em `.gitignore`
- 🔑 Mantenha chaves OpenAI seguras

---

## ❓ Troubleshooting

### "Script não encontra .cookies.json"
**Solução:**
```powershell
# Execute login novamente
python scripts\login-facebook.py
```

### "Facebook bloqueia publicação"
**Motivo:** Limite diário de 30 grupos  
**Solução:** Aguarde até o dia seguinte

### "OpenAI retorna erro"
**Solução:**
1. Verifique chave no `.env`
2. Verifique saldo OpenAI
3. Pague para continuar usando

### "Navegador fecha sozinho"
**Solução:** Use `--headed` para ver o que acontece:
```powershell
python scripts\publish_groups_playwright.py --headed
```

### "Cookies expirados"
**Solução:** Faça login novamente:
```powershell
python scripts\login-facebook.py
```

---

## 📈 Automação Contínua

Para rodar automaticamente a cada dia:

1. Use o script de Messenger (Task Scheduler):
   - Localização: `scheduled-tasks/impar-messenger-inbox/`
   - Executa a cada 5 minutos
   - Responde mensagens automaticamente

2. Crie sua própria tarefa agendada:
   ```powershell
   # Ver: scheduled-tasks/README.md
   ```

---

## ✨ Resultado Final

Após seguir esses passos:

✅ Facebook conectado via cookies  
✅ Anúncios publicados nos 96 grupos  
✅ Leads capturados automaticamente  
✅ Respostas de Messenger automáticas  
✅ Tudo rodando 24/7  

---

**Status:** 🟢 Pronto para conectar!  
**Próximo passo:** Execute `python scripts\login-facebook.py`
