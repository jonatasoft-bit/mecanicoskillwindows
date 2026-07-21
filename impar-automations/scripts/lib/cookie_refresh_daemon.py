#!/usr/bin/env python3
"""
Daemon de Renovação de Cookies
Monitora expiração de cookies e faz refresh automático
Pode rodar como serviço do Windows ou cron job
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from .cookie_manager import CookieManager
from .credentials_manager import CredentialsManager
from .logger_config import get_logger
from .notifier import Notifier

logger = get_logger()


class CookieRefreshDaemon:
    """Daemon para renovação automática de cookies"""

    def __init__(self, base_dir: Path = None, auto_start: bool = False):
        """
        Inicializa o daemon

        Args:
            base_dir: Diretório raiz do projeto
            auto_start: Se deve iniciar o daemon imediatamente
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = base_dir
        self.cookie_manager = CookieManager(base_dir)
        self.creds_manager = CredentialsManager(base_dir)
        self.notifier = Notifier(base_dir)
        self.logs_dir = base_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        self.status_file = self.logs_dir / "refresh_daemon.json"

        load_dotenv(base_dir / ".env")

        if auto_start:
            self.run_once()

    def check_and_refresh(self, days_threshold: int = 30, force: bool = False) -> dict:
        """
        Verifica cookies e faz refresh se necessário

        Args:
            days_threshold: Dias para trigger refresh (padrão: 30)
            force: Forçar refresh mesmo se não vencido

        Returns:
            Dict com resultado da operação
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "action": "check_and_refresh",
            "cookies_valid": False,
            "cookies_need_refresh": False,
            "refresh_attempted": False,
            "refresh_success": False,
            "error": None,
            "days_until_expiry": -1
        }

        try:
            # Verificar cookies
            if not self.cookie_manager.is_valid():
                status["error"] = "Cookies não encontrados ou expirados"
                logger.warning("Cookies não válidos, refresh necessário")
                self.notifier.notify_cookie_expiring_soon(0)
                return status

            status["cookies_valid"] = True
            days_left = self.cookie_manager.days_until_expiry()
            status["days_until_expiry"] = days_left

            # Verificar se precisa refresh
            needs_refresh = (days_left < days_threshold) or force

            if not needs_refresh:
                status["cookies_need_refresh"] = False
                logger.info(f"Cookies válidos por mais {days_left} dias, refresh desnecessário")
                return status

            status["cookies_need_refresh"] = True
            logger.info(f"Cookies precisam refresh ({days_left} dias restantes)")

            # Verificar credenciais
            if not self.creds_manager.has_credentials():
                status["error"] = "Credenciais não salvas, não posso fazer refresh automático"
                logger.error("Credenciais não encontradas para refresh automático")
                self.notifier.notify_cookie_expiring_soon(days_left)
                return status

            # Fazer refresh automático
            status["refresh_attempted"] = True
            logger.info("Tentando refresh automático de cookies...")

            success = self._refresh_cookies_automatic()

            if success:
                status["refresh_success"] = True
                logger.info("Refresh automático concluído com sucesso")
                self.notifier.notify_login_success()
            else:
                status["error"] = "Refresh automático falhou"
                logger.error("Refresh automático falhou")
                self.notifier.notify_cookie_expiring_soon(days_left)

            return status

        except Exception as e:
            status["error"] = str(e)
            logger.error(f"Erro em check_and_refresh: {e}", exc_info=True)
            return status

    def _refresh_cookies_automatic(self) -> bool:
        """
        Faz refresh automático usando credenciais

        Returns:
            True se bem-sucedido
        """
        try:
            # Importar aqui para evitar dependência circular
            import sys
            from pathlib import Path

            # Obter módulo de login automático
            scripts_path = Path(__file__).parent.parent
            sys.path.insert(0, str(scripts_path))

            # Executar login automático
            from login_facebook_automated import main as auto_login

            # Capturar stdout para não imprimir
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                result = auto_login()
                sys.stdout = old_stdout
                return result == 0
            except Exception as e:
                sys.stdout = old_stdout
                logger.error(f"Erro no login automático: {e}")
                return False

        except Exception as e:
            logger.error(f"Erro ao fazer refresh: {e}", exc_info=True)
            return False

    def run_once(self, days_threshold: int = 30, force: bool = False) -> bool:
        """
        Executa verificação uma vez (para Task Scheduler)

        Args:
            days_threshold: Dias para trigger refresh
            force: Forçar refresh

        Returns:
            True se refresh bem-sucedido ou desnecessário
        """
        logger.info("=== Cookie Refresh Daemon Iniciado ===")

        try:
            result = self.check_and_refresh(days_threshold, force)
            self._save_status(result)

            success = result.get("refresh_success", False)
            cookies_valid = result.get("cookies_valid", False)

            if cookies_valid and (result.get("refresh_attempted") == False or success):
                logger.info("Daemon completado com sucesso")
                return True
            else:
                logger.warning("Daemon completado com avisos/erros")
                return False

        except Exception as e:
            logger.error(f"Erro fatal no daemon: {e}", exc_info=True)
            return False

    def _save_status(self, status: dict):
        """Salva status do daemon em arquivo"""
        try:
            with open(self.status_file, 'w') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar status: {e}")

    def get_status(self) -> dict:
        """Obtém último status do daemon"""
        try:
            if not self.status_file.exists():
                return None

            with open(self.status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao ler status: {e}")
            return None


def run_daemon_once():
    """Função de entrada para Task Scheduler"""
    daemon = CookieRefreshDaemon()
    success = daemon.run_once()
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    exit_code = run_daemon_once()
    sys.exit(exit_code)
