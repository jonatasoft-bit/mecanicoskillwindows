#!/usr/bin/env python3
"""
Gerenciador de Credenciais Encriptadas
Armazena email/senha com encriptação Fernet segura
"""

import os
import json
from pathlib import Path
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key


class CredentialsManager:
    """Gerencia credenciais encriptadas para login automático"""

    def __init__(self, base_dir: Path = None):
        """
        Inicializa o gerenciador de credenciais

        Args:
            base_dir: Diretório raiz do projeto (padrão: parent de scripts)
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = base_dir
        self.env_file = base_dir / ".env"
        self.encrypted_file = base_dir / ".env.encrypted"
        self.key_file = base_dir / ".fernet.key"

        load_dotenv(self.env_file)

        self._ensure_key()

    def _ensure_key(self):
        """Garante que a chave Fernet existe"""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)

    def _get_cipher(self) -> Fernet:
        """Obtém a cifra Fernet com a chave armazenada"""
        with open(self.key_file, 'rb') as f:
            key = f.read()
        return Fernet(key)

    def save_credentials(self, email: str, password: str, backup_codes: list = None) -> bool:
        """
        Salva credenciais encriptadas

        Args:
            email: Email do Facebook
            password: Senha do Facebook
            backup_codes: Códigos de backup para 2FA (opcional)

        Returns:
            True se salvo com sucesso
        """
        try:
            cipher = self._get_cipher()

            credentials = {
                "email": email,
                "password": password,
                "backup_codes": backup_codes or []
            }

            json_str = json.dumps(credentials)
            encrypted = cipher.encrypt(json_str.encode())

            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted)

            os.chmod(self.encrypted_file, 0o600)

            set_key(self.env_file, "FACEBOOK_CREDENTIALS_ENCRYPTED", "true")

            return True
        except Exception as e:
            print(f"❌ Erro ao salvar credenciais: {e}")
            return False

    def load_credentials(self) -> dict:
        """
        Carrega credenciais encriptadas

        Returns:
            Dict com email, password, backup_codes
        """
        try:
            if not self.encrypted_file.exists():
                return None

            cipher = self._get_cipher()

            with open(self.encrypted_file, 'rb') as f:
                encrypted = f.read()

            decrypted = cipher.decrypt(encrypted)
            credentials = json.loads(decrypted.decode())

            return credentials
        except Exception as e:
            print(f"❌ Erro ao carregar credenciais: {e}")
            return None

    def has_credentials(self) -> bool:
        """Verifica se credenciais estão armazenadas"""
        return self.encrypted_file.exists()

    def delete_credentials(self) -> bool:
        """Deleta credenciais armazenadas"""
        try:
            if self.encrypted_file.exists():
                os.remove(self.encrypted_file)
            set_key(self.env_file, "FACEBOOK_CREDENTIALS_ENCRYPTED", "false")
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar credenciais: {e}")
            return False

    def update_backup_codes(self, backup_codes: list) -> bool:
        """Atualiza apenas os códigos de backup"""
        try:
            credentials = self.load_credentials()
            if not credentials:
                return False

            credentials["backup_codes"] = backup_codes
            return self.save_credentials(
                credentials["email"],
                credentials["password"],
                backup_codes
            )
        except Exception as e:
            print(f"❌ Erro ao atualizar backup codes: {e}")
            return False
