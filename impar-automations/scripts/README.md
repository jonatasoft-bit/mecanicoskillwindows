# Scripts Python - Impar Automacoes

Este diretorio contem 23 scripts Python para:

- **Geradores de Fila** (generate_queue.py, generate_group_queue.py)
- **Publicadores** (publish_groups_playwright.py, publish_marketplace_playwright.py)
- **Utilitarios** (openai_enhance.py, login-facebook.py, fetch_group_urls.py)
- **Debuggers** (debug-form.py, debug-iframes.py, probe_form.py)
- **Testes** (test_price_extraction.py, test_cadencia_nova.py, test_enhance.py)

Os scripts devem ser extraidos do arquivo ZIP `impar-facebook-automations-windows.zip` do arquivo ZIP fornecido.

## Como Adicionar

1. Extraia o arquivo ZIP
2. Copie todos os arquivos `.py` do diretorio `scripts/` para este diretorio
3. Execute o instalador novamente

## Primeiros Scripts a Usar

```powershell
# Gerar fila marketplace
python generate_queue.py

# Gerar fila de grupos
python generate_group_queue.py

# Publicar em grupos (preview)
python publish_groups_playwright.py --headed
```

Veja README.md na raiz do diretorio impar-automations para mais detalhes.
