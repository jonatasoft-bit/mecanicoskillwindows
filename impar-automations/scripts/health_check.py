#!/usr/bin/env python3
"""
Health Check - Verificar Status de Autenticação
Valida credenciais, cookies, e estado do sistema
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "lib"))

from lib.credentials_manager import CredentialsManager
from lib.cookie_manager import CookieManager
from lib.session_validator import SessionValidator


def main():
    print("=" * 70)
    print("Impar Automations - Health Check")
    print("=" * 70)

    base_dir = Path(__file__).parent.parent

    # Verificar Credenciais
    print("\n📋 Verificando Credenciais...")
    creds_manager = CredentialsManager(base_dir)

    if creds_manager.has_credentials():
        creds = creds_manager.load_credentials()
        if creds:
            email = creds.get("email", "")
            email_masked = email[:3] + "***" + email[-8:] if len(email) > 11 else "***"
            print(f"   ✅ Credenciais encontradas: {email_masked}")
        else:
            print("   ⚠️ Credenciais corrompidas ou ilegíveis")
    else:
        print("   ❌ Nenhuma credencial salva")

    # Verificar Cookies
    print("\n🍪 Verificando Cookies...")
    cookie_manager = CookieManager(base_dir)
    status = cookie_manager.get_status()

    print(f"   Status: {status.get('status', 'desconhecido')}")
    if status.get('valid'):
        print(f"   ✅ Cookies válidos")
        print(f"   📅 Salvo em: {status.get('saved_at', 'N/A')[:10]}")
        print(f"   ⏰ Expira em: {status.get('expires_at', 'N/A')[:10]}")
        print(f"   ⏳ Dias restantes: {status.get('days_until_expiry', 0)}")
        if status.get('needs_refresh'):
            print(f"   ⚠️ PRECISA REFRESH em breve!")
    else:
        print(f"   ❌ Cookies inválidos ou expirados")

    # Validar Sessão
    print("\n🔐 Validando Sessão...")
    validator = SessionValidator(base_dir)
    validation = validator.validate_before_action("health_check")

    print(f"   Sessão ativa: {'✅ Sim' if validation['session_valid'] else '❌ Não'}")
    print(f"   Pode prosseguir: {'✅ Sim' if validation['can_proceed'] else '❌ Não'}")
    print(f"   Precisa refresh: {'⚠️ Sim' if validation['needs_refresh'] else '✅ Não'}")

    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DO STATUS")
    print("=" * 70)

    has_creds = creds_manager.has_credentials()
    cookies_valid = cookie_manager.is_valid()
    session_active = validator.is_logged_in()

    if has_creds and cookies_valid and session_active:
        print("✅ Sistema pronto para usar!")
        print("   - Credenciais: OK")
        print("   - Cookies: OK")
        print("   - Sessão: OK")
        return 0
    else:
        print("⚠️ Sistema necessita de configuração:")
        if not has_creds:
            print("   ❌ Credenciais não configuradas")
        if not cookies_valid:
            print("   ❌ Cookies não válidos")
        if not session_active:
            print("   ❌ Sessão inativa")

        print("\n📝 Próximos passos:")
        if not has_creds or not cookies_valid:
            print("   1. Execute: python scripts\\login-facebook-interactive.py")
        if not session_active and has_creds:
            print("   2. Tente refresh automático: python scripts\\login-facebook-automated.py")

        return 1


if __name__ == "__main__":
    sys.exit(main())
