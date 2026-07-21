#!/usr/bin/env python3
"""
Impar Automacoes - Login Facebook via Chrome
Realiza autenticacao no Facebook usando Google Chrome especificamente
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv, set_key

try:
    from playwright.sync_api import sync_playwright
    import time
except ImportError:
    print("❌ Erro: Playwright nao esta instalado")
    print("   Execute: pip install playwright")
    print("   Depois: python -m playwright install chromium")
    sys.exit(1)

def main():
    print("=" * 70)
    print("Impar Automacoes - Login Facebook via Chrome")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env"

    load_dotenv(env_file)

    print("\n🌐 Abrindo CHROME para login no Facebook...")
    print("   Siga as instrucoes na tela do navegador")
    print("   Faça login com sua conta do Facebook")
    print("   NÃO feche o navegador até terminar!\n")

    with sync_playwright() as p:
        # Tentar usar Chrome primeiro
        try:
            print("▶ Tentando Chrome...")

            # Verificar se Chrome está instalado
            try:
                browser = p.chromium.launch(
                    headless=False,
                    channel="chrome"  # Força uso do Chrome do sistema
                )
                print("✓ Chrome aberto")
            except Exception as e:
                print(f"⚠ Chrome do sistema não encontrado: {e}")
                print("   Tentando Chromium (navegador embutido)...")
                browser = p.chromium.launch(headless=False)
                print("✓ Chromium aberto")

        except Exception as e:
            print(f"❌ Erro ao abrir navegador: {e}")
            print("   Tente instalar: python -m playwright install chromium")
            return 1

        context = browser.new_context()
        page = context.new_page()

        # Navegar para Facebook Marketplace
        print("\n▶ Navegando para Facebook Marketplace...")
        try:
            page.goto("https://www.facebook.com/marketplace/", timeout=30000)
            print("✓ Página carregada")
        except Exception as e:
            print(f"⚠ Erro ao navegar: {e}")

        print("\n⏳ Aguardando login (máx 10 minutos)...")
        print("   Passos:")
        print("   1. Digite seu email ou telefone")
        print("   2. Digite sua senha")
        print("   3. Confirme 2FA se solicitado")
        print("   4. Aguarde carregar Marketplace completamente")
        print("   5. Script vai capturar cookies automaticamente\n")

        # Esperar usuario fazer login
        max_wait = 600  # 10 minutos
        wait_interval = 2
        elapsed = 0
        logged_in = False

        while elapsed < max_wait and not logged_in:
            try:
                current_url = page.url

                # Verificar se está na página de Marketplace (logged in)
                if "marketplace" in current_url.lower():
                    # Verificar se login foi realizado
                    try:
                        # Tentar encontrar elemento que só existe se logado
                        page.wait_for_selector('[role="main"]', timeout=2000)

                        # Esperar um pouco mais para garantir carregamento
                        time.sleep(2)

                        logged_in = True
                        print("\n✓ Login detectado com sucesso!")
                        break
                    except:
                        pass

            except Exception as e:
                pass

            time.sleep(wait_interval)
            elapsed += wait_interval
            minutos = elapsed // 60
            segundos = elapsed % 60
            print(f"   Aguardando... ({minutos}:{segundos:02d})", end='\r')

        if not logged_in:
            print("\n\n⚠️  Timeout - Login não foi concluído em tempo")
            print("   Tente novamente")
            browser.close()
            return 1

        # Sucesso!
        print("\n\n✓ Conectado ao Facebook Marketplace!")
        print(f"   URL: {page.url}")

        # Capturar cookies
        print("\n📌 Capturando credenciais...")
        cookies = context.cookies()

        if cookies:
            print(f"✓ {len(cookies)} cookies capturados")

            # Mostrar alguns cookies importantes
            for cookie in cookies[:3]:
                if cookie['name'] in ['xs', 'c_user', 'datr']:
                    valor_curto = cookie['value'][:20] + "..."
                    print(f"   ✓ {cookie['name']}: {valor_curto}")

        # Salvar cookies
        print("\n💾 Salvando credenciais...")
        cookies_file = base_dir / ".cookies.json"

        if cookies:
            cookies_json = json.dumps(cookies, indent=2)
            with open(cookies_file, 'w') as f:
                f.write(cookies_json)
            print(f"   ✓ Cookies salvos em: .cookies.json")

        # Atualizar .env
        set_key(env_file, "FACEBOOK_MARKETPLACE_URL", "https://www.facebook.com/marketplace/")
        set_key(env_file, "FACEBOOK_LOGGED_IN", "true")
        print(f"   ✓ .env atualizado")

        browser.close()

    print("\n" + "=" * 70)
    print("✅ LOGIN CONCLUIDO COM SUCESSO!")
    print("=" * 70)
    print("\n📝 Seus cookies foram salvos automaticamente!")
    print("   Arquivo: .cookies.json")
    print("\n🚀 Proximos passos:")
    print("   1. Gerar fila marketplace:")
    print("      python scripts\\generate_queue.py")
    print("")
    print("   2. Gerar fila de grupos:")
    print("      python scripts\\generate_group_queue.py")
    print("")
    print("   3. Visualizar antes de publicar:")
    print("      python scripts\\publish_groups_playwright.py --headed")
    print("")
    print("   4. Publicar nos grupos:")
    print("      python scripts\\publish_groups_playwright.py --headed --publish")
    print("\n⚠️  IMPORTANTE: Mantenha .cookies.json seguro!")
    print("   Não compartilhe com ninguém e não commite em repositório público!")

    return 0

if __name__ == "__main__":
    sys.exit(main())
