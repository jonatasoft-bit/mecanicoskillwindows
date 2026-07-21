#!/usr/bin/env python3
"""
Notificador de Eventos
Envia notificações via WhatsApp quando algo importante acontece
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

try:
    import requests
except ImportError:
    requests = None


class Notifier:
    """Gerencia notificações de eventos"""

    def __init__(self, base_dir: Path = None):
        """
        Inicializa notificador

        Args:
            base_dir: Diretório raiz do projeto
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = base_dir
        load_dotenv(base_dir / ".env")

        self.whatsapp_webhook = os.getenv("WHATSAPP_WEBHOOK_URL")
        self.whatsapp_enabled = bool(self.whatsapp_webhook)
        self.logs_dir = base_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)

    def notify_login_failure(self, error: str, attempt: int = 1, max_attempts: int = 3):
        """Notifica falha no login automático"""
        message = f"❌ Login Facebook falhou (tentativa {attempt}/{max_attempts})\n"
        message += f"Erro: {error}\n"
        message += f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        self._send_notification("login_failure", message, severity="high")

    def notify_login_success(self):
        """Notifica sucesso no login"""
        message = "✅ Login Facebook automático concluído com sucesso!\n"
        message += f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        self._send_notification("login_success", message, severity="low")

    def notify_cookie_expiring_soon(self, days_left: int):
        """Notifica que cookies vão expirar em breve"""
        message = f"⏰ Cookies do Facebook expiram em {days_left} dias\n"
        message += "Será feito refresh automático em breve.\n"
        message += f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        self._send_notification("cookie_expiring", message, severity="medium")

    def notify_publishing_failure(self, groups_failed: int, error: str):
        """Notifica falha na publicação"""
        message = f"⚠️ Falha ao publicar em {groups_failed} grupo(s)\n"
        message += f"Erro: {error}\n"
        message += f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        self._send_notification("publishing_failure", message, severity="medium")

    def notify_publishing_success(self, groups_count: int, listings_count: int):
        """Notifica sucesso na publicação"""
        message = f"✅ Publicação concluída com sucesso!\n"
        message += f"📍 {groups_count} grupos publicados\n"
        message += f"🏠 {listings_count} imóveis processados\n"
        message += f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        self._send_notification("publishing_success", message, severity="low")

    def notify_daily_status(self, stats: dict):
        """Notifica status diário de operações"""
        message = "📊 Relatório Diário Impar Automations\n"
        message += f"✅ Logins: {stats.get('logins_success', 0)}\n"
        message += f"❌ Falhas: {stats.get('logins_failure', 0)}\n"
        message += f"📍 Grupos publicados: {stats.get('groups_published', 0)}\n"
        message += f"🏠 Imóveis publicados: {stats.get('listings_published', 0)}\n"
        message += f"Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        self._send_notification("daily_status", message, severity="low")

    def _send_notification(self, event_type: str, message: str, severity: str = "info"):
        """
        Envia notificação via WhatsApp

        Args:
            event_type: Tipo de evento
            message: Mensagem a enviar
            severity: Severidade (low, medium, high)
        """
        # Log do evento
        self._log_event(event_type, message, severity)

        # Enviar via WhatsApp se configurado
        if self.whatsapp_enabled:
            self._send_whatsapp(message, severity)

    def _send_whatsapp(self, message: str, severity: str):
        """Envia mensagem via WhatsApp webhook"""
        if not requests:
            print("⚠️ Requests não instalado, pulando notificação WhatsApp")
            return

        try:
            payload = {
                "message": message,
                "severity": severity,
                "timestamp": datetime.now().isoformat()
            }

            response = requests.post(
                self.whatsapp_webhook,
                json=payload,
                timeout=10
            )

            if response.status_code not in [200, 201]:
                print(f"⚠️ Erro ao enviar WhatsApp: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Erro ao enviar WhatsApp: {e}")

    def _log_event(self, event_type: str, message: str, severity: str):
        """Registra evento em log local"""
        log_file = self.logs_dir / "notifications.json"

        try:
            # Carregar logs existentes
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []

            # Adicionar novo evento
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "severity": severity,
                "message": message
            })

            # Manter apenas últimos 1000 eventos
            logs = logs[-1000:]

            # Salvar
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao registrar notificação: {e}")

    def get_recent_events(self, limit: int = 10) -> list:
        """Obtém eventos recentes"""
        log_file = self.logs_dir / "notifications.json"

        try:
            if not log_file.exists():
                return []

            with open(log_file, 'r') as f:
                logs = json.load(f)

            return logs[-limit:]
        except Exception:
            return []
