#!/usr/bin/env python3
"""
Login Facebook Automático - Headless
Faz login automático sem necessidade de interação humana
Usa Playwright stealth mode para parecer browser normal
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv, set_key

sys.path.insert(0, str(Path(__file__).parent / "lib"))

from lib.credentials_manager import CredentialsManager
from lib.cookie_manager import CookieManager
from lib.retry_handler import RetryHandler
from lib.logger_config import setup_logging
from lib.notifier import Notifier

try:
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync
except ImportError:
    print("❌ Erro: Playwright ou Stealth não estão instalados")
    print("   Execute: pip install playwright playwright-stealth")
    print("   Depois: python -m playwright install chromium")
    sys.exit(1)


logger = setup_logging()


def login_with_credentials(page, email: str, password: str, timeout: int = 30):
    """
    Faz login com credenciais automaticamente

    Args:
        page: Página do Playwright
        email: Email do Facebook
        password: Senha do Facebook
        timeout: Timeout em segundos

    Raises:
        Exception: Se login falhar
    """
    print("▶ Preenchendo credenciais...")

    # Aguardar campo de email
    page.wait_for_selector('input[name="email"]', timeout=timeout * 1000)
    page.fill('input[name="email"]', email)

    # Preencher senha
    page.fill('input[name="pass"]', password)

    # Clicar botão login
    page.click('button[name="login"]')

    print("⏳ Aguardando confirmação de login...")

    # Aguardar redirecionamento para marketplace ou página de verificação
    try:
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)
    except:
        pass

    # Verificar sucesso
    current_url = page.url
    if "facebook.com" not in current_url:
        raise Exception(f"Redirecionamento inesperado para: {current_url}")

    # Aguardar elemento que indica login bem-sucedido
    try:
        page.wait_for_selector('[role="main"]', timeout=5 * 1000)
        print("✓ Login confirmado")
        return True
    except:
        raise Exception("Login não confirmado - elemento de validação não encontrado")


def main():
    print("=" * 70)
    print("Impar Automations - Login Facebook Automático")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env"

    load_dotenv(env_file)

    # Inicializar managers
    creds_manager = CredentialsManager(base_dir)
    cookie_manager = CookieManager(base_dir)
    notifier = Notifier(base_dir)

    print("\n🔐 Verificando credenciais...")

    # Carregar credenciais
    credentials = creds_manager.load_credentials()
    if not credentials:
        print("❌ Nenhuma credencial salva!")
        print("   Execute: python scripts\\login-facebook-interactive.py")
        logger.error("Credenciais não encontradas")
        return 1

    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        print("❌ Credenciais incompletas ou corrompidas!")
        logger.error("Credenciais incompletas")
        return 1

    print(f"✓ Credenciais carregadas")

    # Configurar retry
    retry_handler = RetryHandler(
        max_attempts=3,
        initial_delay=2,
        max_delay=32
    )

    def on_retry_error(attempt, error, delay):
        msg = f"Tentativa {attempt} falhou: {error}"
        print(f"⚠ {msg}")
        if delay > 0:
            print(f"  Aguardando {delay}s...")
        logger.warning(msg)

    def login_attempt():
        """Tenta fazer login"""
        print("\n🌐 Iniciando navegador (headless)...")

        with sync_playwright() as p:
            try:
                # Tentar Chrome do sistema primeiro
                try:
                    browser = p.chromium.launch(
                        headless=True,
                        channel="chrome"
                    )
                except:
                    browser = p.chromium.launch(headless=True)

                context = browser.new_context()
                page = context.new_page()

                # Aplicar stealth mode
                stealth_sync(page)

                # Navigar para marketplace
                print("▶ Acessando Facebook Marketplace...")
                page.goto("https://www.facebook.com/marketplace/", timeout=30000)

                # Fazer login
                login_with_credentials(page, email, password, timeout=30)

                # Capturar cookies
                print("\n📌 Capturando cookies...")
                cookies = context.cookies()

                if not cookies:
                    raise Exception("Nenhum cookie foi capturado")

                print(f"✓ {len(cookies)} cookies capturados")

                # Salvar cookies
                print("💾 Salvando cookies...")
                if cookie_manager.save_cookies(cookies):
                    print("✓ Cookies salvos com sucesso")
                    set_key(env_file, "FACEBOOK_LOGGED_IN", "true")
                else:
                    raise Exception("Falha ao salvar cookies")

                browser.close()
                return True

            except Exception as e:
                print(f"❌ Erro durante login: {e}")
                try:
                    browser.close()
                except:
                    pass
                raise

    # Executar com retry
    try:
        retry_handler.execute(
            login_attempt,
            on_error=on_retry_error
        )
    except Exception as e:
        print(f"\n❌ LOGIN FALHOU APÓS {retry_handler.attempts} TENTATIVAS")
        print(f"   Erro final: {e}")
        logger.error(f"Login automático falhou: {e}", exc_info=True)
        notifier.notify_login_failure(str(e), retry_handler.attempts, 3)
        return 1

    # Sucesso!
    print("\n" + "=" * 70)
    print("✅ LOGIN AUTOMÁTICO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)

    print("\n✓ Sistema pronto para publicação automática")
    print("   Cookies válidos por: 60 dias")
    print("   Próxima renovação: em ~55 dias")

    logger.info("Login automático concluído com sucesso")
    notifier.notify_login_success()

    return 0


if __name__ == "__main__":
    sys.exit(main())
