#!/usr/bin/env python3
"""
Impar Automacoes - Login Facebook
Realiza autenticacao no Facebook e captura tokens necessarios
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv, set_key

# Verificar se playwright esta instalado
try:
    from playwright.sync_api import sync_playwright
    import time
except ImportError:
    print("❌ Erro: Playwright nao esta instalado")
    print("   Execute: pip install playwright")
    print("   Depois: python -m playwright install chromium")
    sys.exit(1)

def main():
    print("=" * 60)
    print("Impar Automacoes - Login Facebook")
    print("=" * 60)

    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env"

    # Carregar .env existente
    load_dotenv(env_file)

    print("\n📱 Abrindo navegador para login no Facebook...")
    print("   Siga as instrucoes na tela do navegador")
    print("   Faça login com sua conta do Facebook")
    print("   Não feche o navegador até terminar!\n")

    with sync_playwright() as p:
        # Abrir navegador com modo headed (visível)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navegar para Facebook Marketplace
        print("▶ Navegando para Facebook Marketplace...")
        page.goto("https://www.facebook.com/marketplace/")

        print("⏳ Aguardando login (máx 5 minutos)...")
        print("   Passos:")
        print("   1. Digite seu email/telefone")
        print("   2. Digite sua senha")
        print("   3. Confirme 2FA se solicitado")
        print("   4. Aguarde carregar Marketplace completamente")

        # Esperar usuario fazer login (máximo 5 minutos)
        max_wait = 300  # 5 minutos
        wait_interval = 2
        elapsed = 0
        logged_in = False

        while elapsed < max_wait and not logged_in:
            try:
                # Verificar se esta na pagina de Marketplace (indicativo de login)
                if "marketplace" in page.url.lower() or "facebook" in page.url.lower():
                    # Verificar se o botao de login desapareceu
                    login_button = page.query_selector('button:has-text("Log In")')
                    if not login_button:
                        # Esperar um pouco mais para garantir que carregou
                        time.sleep(3)

                        # Tentar pegar titulo da pagina
                        title = page.title()
                        if title and "facebook" in title.lower():
                            logged_in = True
                            print("\n✓ Login realizado com sucesso!")
                            break
            except:
                pass

            time.sleep(wait_interval)
            elapsed += wait_interval
            print(f"   Aguardando... ({elapsed//60}:{elapsed%60:02d})")

        if not logged_in:
            print("\n⚠️  Timeout - Login nao foi concluido em tempo")
            print("   Tente novamente")
            browser.close()
            return 1

        # Extrair URL atual (tem informacoes uteis)
        print("\n✓ Conectado ao Facebook Marketplace")
        current_url = page.url
        print(f"   URL: {current_url}")

        # Capturar cookies e tokens
        print("\n📌 Capturando credenciais...")
        cookies = context.cookies()

        # Procurar tokens importantes
        facebook_token = None
        user_id = None

        for cookie in cookies:
            if cookie['name'] == 'xs' or cookie['name'] == 'c_user':
                print(f"   ✓ {cookie['name']}: {cookie['value'][:20]}...")

        # Salvar informacoes no .env
        print("\n💾 Salvando credenciais em .env...")

        # Salvar URL de cookies (pode ser util)
        if cookies:
            cookies_json = json.dumps(cookies, indent=2)
            # Salvar em arquivo separado (nao no .env por seguranca)
            cookies_file = base_dir / ".cookies.json"
            with open(cookies_file, 'w') as f:
                f.write(cookies_json)
            print(f"   ✓ Cookies salvos em: {cookies_file}")

        # Salvar URLs importantes
        set_key(env_file, "FACEBOOK_MARKETPLACE_URL", "https://www.facebook.com/marketplace/")
        print(f"   ✓ .env atualizado")

        browser.close()

    print("\n" + "=" * 60)
    print("✅ LOGIN CONCLUIDO COM SUCESSO!")
    print("=" * 60)
    print("\n📝 Próximos passos:")
    print("   1. Seus cookies foram salvos em: .cookies.json")
    print("   2. Agora você pode rodar os scripts de automacao:")
    print("      - python scripts\\generate_queue.py")
    print("      - python scripts\\generate_group_queue.py")
    print("   3. IMPORTANTE: Mantenha .cookies.json seguro!")
    print("      (Nao commit em repositorio publico!)")

    return 0

if __name__ == "__main__":
    sys.exit(main())
