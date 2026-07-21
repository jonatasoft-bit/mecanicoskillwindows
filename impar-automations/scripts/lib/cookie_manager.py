#!/usr/bin/env python3
"""
Gerenciador de Cookies com Validação de Expiração
Valida, salva e carrega cookies com timestamp
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta


class CookieManager:
    """Gerencia cookies com validação de expiração"""

    REQUIRED_COOKIES = ["c_user", "xs", "datr"]
    COOKIE_EXPIRY_DAYS = 60

    def __init__(self, base_dir: Path = None):
        """
        Inicializa o gerenciador de cookies

        Args:
            base_dir: Diretório raiz do projeto
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = base_dir
        self.cookies_file = base_dir / ".cookies.json"
        self.cookies_backup = base_dir / ".cookies.backup.json"

    def save_cookies(self, cookies: list) -> bool:
        """
        Salva cookies com timestamp de expiração

        Args:
            cookies: Lista de cookies do Playwright

        Returns:
            True se salvo com sucesso
        """
        try:
            now = datetime.now()
            expires_at = (now + timedelta(days=self.COOKIE_EXPIRY_DAYS)).isoformat()

            data = {
                "saved_at": now.isoformat(),
                "expires_at": expires_at,
                "days_until_expiry": self.COOKIE_EXPIRY_DAYS,
                "cookies": cookies
            }

            # Backup dos cookies antigos
            if self.cookies_file.exists():
                with open(self.cookies_file, 'r') as f:
                    old_data = json.load(f)
                with open(self.cookies_backup, 'w') as f:
                    json.dump(old_data, f, indent=2)

            # Salvar novos cookies
            with open(self.cookies_file, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Erro ao salvar cookies: {e}")
            return False

    def load_cookies(self) -> list:
        """
        Carrega cookies se ainda forem válidos

        Returns:
            Lista de cookies ou None se expirado/não encontrado
        """
        try:
            if not self.cookies_file.exists():
                return None

            with open(self.cookies_file, 'r') as f:
                data = json.load(f)

            cookies = data.get("cookies", [])

            if not self._validate_cookies(cookies):
                return None

            return cookies
        except Exception as e:
            print(f"❌ Erro ao carregar cookies: {e}")
            return None

    def is_valid(self) -> bool:
        """Verifica se cookies são válidos (não expirados)"""
        try:
            if not self.cookies_file.exists():
                return False

            with open(self.cookies_file, 'r') as f:
                data = json.load(f)

            expires_at = datetime.fromisoformat(data.get("expires_at", ""))
            now = datetime.now()

            return now < expires_at
        except Exception:
            return False

    def days_until_expiry(self) -> int:
        """Retorna dias até expiração dos cookies"""
        try:
            if not self.cookies_file.exists():
                return -1

            with open(self.cookies_file, 'r') as f:
                data = json.load(f)

            expires_at = datetime.fromisoformat(data.get("expires_at", ""))
            now = datetime.now()
            delta = expires_at - now

            return max(0, delta.days)
        except Exception:
            return -1

    def needs_refresh(self, days_threshold: int = 30) -> bool:
        """
        Verifica se cookies precisam ser renovados

        Args:
            days_threshold: Dias restantes para trigger refresh (padrão: 30)

        Returns:
            True se cookies precisam refresh
        """
        days_left = self.days_until_expiry()
        return days_left < days_threshold

    def get_status(self) -> dict:
        """Retorna status dos cookies"""
        try:
            if not self.cookies_file.exists():
                return {
                    "status": "não encontrado",
                    "valid": False,
                    "days_until_expiry": -1
                }

            with open(self.cookies_file, 'r') as f:
                data = json.load(f)

            saved_at = data.get("saved_at", "")
            expires_at = data.get("expires_at", "")
            days_left = self.days_until_expiry()
            valid = self.is_valid()

            return {
                "status": "válido" if valid else "expirado",
                "valid": valid,
                "saved_at": saved_at,
                "expires_at": expires_at,
                "days_until_expiry": days_left,
                "needs_refresh": self.needs_refresh()
            }
        except Exception as e:
            return {
                "status": "erro",
                "valid": False,
                "error": str(e)
            }

    def _validate_cookies(self, cookies: list) -> bool:
        """Valida se cookies contêm campos obrigatórios"""
        cookie_names = {c.get("name") for c in cookies}
        return all(req in cookie_names for req in self.REQUIRED_COOKIES)

    def delete_cookies(self) -> bool:
        """Deleta cookies salvos"""
        try:
            if self.cookies_file.exists():
                self.cookies_file.unlink()
            if self.cookies_backup.exists():
                self.cookies_backup.unlink()
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar cookies: {e}")
            return False
