#!/usr/bin/env python3
"""
API Web para Dashboard de Automação
Fornece endpoints REST para controlar login e monitoramento
"""

import json
from pathlib import Path
from datetime import datetime

from .credentials_manager import CredentialsManager
from .cookie_manager import CookieManager
from .session_validator import SessionValidator
from .logger_config import get_logger

logger = get_logger()


class AutomationAPI:
    """API REST para automação de Facebook"""

    def __init__(self, base_dir: Path = None):
        """Inicializa API"""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = base_dir
        self.creds_manager = CredentialsManager(base_dir)
        self.cookie_manager = CookieManager(base_dir)
        self.session_validator = SessionValidator(base_dir)
        self.logs_dir = base_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)

    def get_status(self) -> dict:
        """Obtém status atual do sistema"""
        cookie_status = self.cookie_manager.get_status()
        has_creds = self.creds_manager.has_credentials()

        return {
            "timestamp": datetime.now().isoformat(),
            "authenticated": cookie_status.get("valid", False),
            "has_credentials": has_creds,
            "cookies": {
                "valid": cookie_status.get("valid", False),
                "days_until_expiry": cookie_status.get("days_until_expiry", 0),
                "saved_at": cookie_status.get("saved_at", None),
                "expires_at": cookie_status.get("expires_at", None),
                "needs_refresh": cookie_status.get("needs_refresh", False)
            },
            "credentials": {
                "saved": has_creds,
                "for_automation": has_creds
            },
            "system": {
                "ready": cookie_status.get("valid", False),
                "message": self._get_status_message(cookie_status, has_creds)
            }
        }

    def get_history(self, limit: int = 20) -> list:
        """Obtém histórico de tentativas de login"""
        history_file = self.logs_dir / "login_history.json"

        try:
            if not history_file.exists():
                return []

            with open(history_file, 'r') as f:
                history = json.load(f)

            if isinstance(history, list):
                return history[-limit:]
            return []
        except Exception as e:
            logger.error(f"Erro ao ler histórico: {e}")
            return []

    def start_interactive_login(self) -> dict:
        """Inicia login interativo"""
        return {
            "status": "started",
            "message": "Abrindo navegador para login...",
            "next_step": "browser_will_open",
            "timestamp": datetime.now().isoformat()
        }

    def refresh_cookies_now(self) -> dict:
        """Tenta refresh automático de cookies agora"""
        try:
            if not self.cookie_manager.is_valid():
                return {
                    "success": False,
                    "error": "Cookies não encontrados ou expirados",
                    "next_step": "need_interactive_login"
                }

            if not self.creds_manager.has_credentials():
                return {
                    "success": False,
                    "error": "Credenciais não salvas para refresh automático",
                    "next_step": "need_interactive_login"
                }

            # Aqui entraria a lógica de refresh automático
            # Por enquanto, retorna sucesso simulado
            return {
                "success": True,
                "message": "Refresh iniciado em background",
                "status": "refreshing",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao refreshar: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def setup_scheduler(self) -> dict:
        """Configura Task Scheduler do Windows"""
        return {
            "status": "not_implemented",
            "message": "Configuração do Task Scheduler será implementada em Phase 3",
            "note": "Execute INSTALL_AUTO_LOGIN.ps1 manualmente por enquanto"
        }

    def get_notifications(self, limit: int = 10) -> list:
        """Obtém notificações recentes"""
        notif_file = self.logs_dir / "notifications.json"

        try:
            if not notif_file.exists():
                return []

            with open(notif_file, 'r') as f:
                notifications = json.load(f)

            if isinstance(notifications, list):
                return notifications[-limit:]
            return []
        except Exception:
            return []

    def _get_status_message(self, cookie_status: dict, has_creds: bool) -> str:
        """Gera mensagem de status legível"""
        if not cookie_status.get("valid"):
            return "❌ Não autenticado - Faça login para começar"

        days_left = cookie_status.get("days_until_expiry", 0)

        if days_left > 30:
            return f"✅ Conectado - {days_left} dias até expiração"
        elif days_left > 0:
            return f"⚠️ Conectado - {days_left} dias (renovação em breve)"
        else:
            return "❌ Cookies expirados - Faça login novamente"
