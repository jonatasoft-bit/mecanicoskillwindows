#!/usr/bin/env python3
"""
Validador de Sessão
Valida cookies e detecta logout inesperado
"""

from pathlib import Path
from .cookie_manager import CookieManager


class SessionValidator:
    """Valida sessão do usuário no Facebook"""

    def __init__(self, base_dir: Path = None):
        """
        Inicializa validador de sessão

        Args:
            base_dir: Diretório raiz do projeto
        """
        self.cookie_manager = CookieManager(base_dir)

    def is_logged_in(self) -> bool:
        """Verifica se há sessão ativa (cookies válidos)"""
        return self.cookie_manager.is_valid()

    def check_cookies_validity(self) -> dict:
        """
        Verifica validade dos cookies

        Returns:
            Dict com status, dias até expiração, etc
        """
        return self.cookie_manager.get_status()

    def should_refresh(self, days_threshold: int = 30) -> bool:
        """
        Verifica se cookies precisam refresh

        Args:
            days_threshold: Dias restantes para trigger (padrão: 30)

        Returns:
            True se precisa refresh
        """
        return self.cookie_manager.needs_refresh(days_threshold)

    def get_cookies_for_login(self) -> list:
        """
        Obtém cookies para usar em login (se válidos)

        Returns:
            Lista de cookies ou None
        """
        if not self.is_logged_in():
            return None
        return self.cookie_manager.load_cookies()

    def validate_before_action(self, action: str = "publish") -> dict:
        """
        Valida sessão antes de uma ação

        Args:
            action: Tipo de ação (publish, refresh, etc)

        Returns:
            Dict com resultado da validação
        """
        status = self.check_cookies_validity()
        is_valid = self.is_logged_in()

        return {
            "action": action,
            "session_valid": is_valid,
            "cookies_status": status,
            "can_proceed": is_valid,
            "needs_refresh": self.should_refresh(days_threshold=30),
            "days_until_expiry": self.cookie_manager.days_until_expiry()
        }
