#!/usr/bin/env python3
"""
Login Facebook Interativo - Manual
Abre navegador para você fazer login manualmente
Salva credenciais e cookies para automação futura
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv, set_key

sys.path.insert(0, str(Path(__file__).parent / "lib"))

from lib.credentials_manager import CredentialsManager
from lib.cookie_manager import CookieManager
from lib.logger_config import setup_logging
from lib.notifier import Notifier

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Erro: Playwright não está instalado")
    print("   Execute: pip install playwright")
    print("   Depois: python -m playwright install chromium")
    sys.exit(1)


logger = setup_logging()


def main():
    print("=" * 70)
    print("Impar Automations - Login Facebook Interativo")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env"

    load_dotenv(env_file)

    # Inicializar managers
    creds_manager = CredentialsManager(base_dir)
    cookie_manager = CookieManager(base_dir)
    notifier = Notifier(base_dir)

    print("\n🌐 Abrindo navegador para login no Facebook...")
    print("   Siga as instruções na tela")
    print("   Faça login com sua conta do Facebook")
    print("   NÃO feche o navegador até terminar!\n")

    with sync_playwright() as p:
        try:
            # Abrir navegador com modo headed (visível para usuário)
            print("▶ Iniciando navegador...")
            try:
                browser = p.chromium.launch(
                    headless=False,
                    channel="chrome"
                )
            except:
                browser = p.chromium.launch(headless=False)

            context = browser.new_context()
            page = context.new_page()

            # Navegar para Facebook Marketplace
            print("▶ Acessando Facebook Marketplace...")
            page.goto("https://www.facebook.com/marketplace/", timeout=30000)

            print("\n⏳ Aguardando seu login (máx 10 minutos)...")
            print("   Passos:")
            print("   1. Digite seu email ou telefone")
            print("   2. Digite sua senha")
            print("   3. Confirme 2FA se solicitado")
            print("   4. Aguarde Marketplace carregar completamente")
            print("   5. Script vai capturar cookies automaticamente\n")

            # Esperar usuário fazer login (máximo 10 minutos)
            max_wait = 600
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
                            page.wait_for_selector('[role="main"]', timeout=2000)
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
                logger.error("Timeout no login interativo")
                return 1

            # Sucesso!
            print("\n\n✓ Conectado ao Facebook Marketplace!")
            print(f"   URL: {page.url}")

            # Capturar cookies
            print("\n📌 Capturando credenciais...")
            cookies = context.cookies()

            if not cookies:
                raise Exception("Nenhum cookie foi capturado")

            print(f"✓ {len(cookies)} cookies capturados")

            # Mostrar alguns cookies importantes
            for cookie in cookies[:3]:
                if cookie['name'] in ['xs', 'c_user', 'datr']:
                    valor_curto = cookie['value'][:20] + "..."
                    print(f"   ✓ {cookie['name']}: {valor_curto}")

            # Salvar cookies
            print("\n💾 Salvando credenciais...")
            if not cookie_manager.save_cookies(cookies):
                raise Exception("Falha ao salvar cookies")
            print(f"   ✓ Cookies salvos")

            # Perguntar se quer salvar credenciais para automação
            print("\n🔐 Deseja salvar suas credenciais para automação?")
            print("   Isso permite login automático nos próximos 60 dias")
            print("   Credenciais serão encriptadas com segurança")
            response = input("   Salvar credenciais? (s/n): ").strip().lower()

            if response in ['s', 'sim', 'y', 'yes']:
                email = input("   Email do Facebook: ").strip()
                password = input("   Senha do Facebook: ").strip()

                if email and password:
                    if creds_manager.save_credentials(email, password):
                        print("   ✓ Credenciais salvas com segurança")
                        set_key(env_file, "FACEBOOK_CREDENTIALS_ENCRYPTED", "true")
                    else:
                        print("   ⚠️  Erro ao salvar credenciais")
                else:
                    print("   ⚠️  Email/senha não pode estar vazio")

            # Atualizar .env
            set_key(env_file, "FACEBOOK_MARKETPLACE_URL", "https://www.facebook.com/marketplace/")
            set_key(env_file, "FACEBOOK_LOGGED_IN", "true")
            print("   ✓ .env atualizado")

            browser.close()

            print("\n" + "=" * 70)
            print("✅ LOGIN CONCLUÍDO COM SUCESSO!")
            print("=" * 70)

            print("\n📝 Seus cookies foram salvos automaticamente!")
            print("   Arquivo: .cookies.json")

            if creds_manager.has_credentials():
                print("\n✅ Credenciais salvas para automação!")
                print("   Próximo login será automático (headless)")
            else:
                print("\n📌 Sem credenciais armazenadas")
                print("   Próximo login será manual (interativo)")

            print("\n🚀 Próximos passos:")
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

            logger.info("Login interativo concluído com sucesso")
            notifier.notify_login_success()

            return 0

        except Exception as e:
            print(f"\n❌ Erro durante login: {e}")
            try:
                browser.close()
            except:
                pass
            logger.error(f"Erro no login interativo: {e}", exc_info=True)
            return 1


if __name__ == "__main__":
    sys.exit(main())
