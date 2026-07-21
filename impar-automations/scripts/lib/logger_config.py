#!/usr/bin/env python3
"""
Configuração de Logging Estruturado
Logs em JSON com histórico de 90 dias
"""

import logging
import json
from pathlib import Path
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Formata logs como JSON estruturado"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(base_dir: Path = None) -> logging.Logger:
    """
    Configura logging centralizado

    Args:
        base_dir: Diretório raiz do projeto

    Returns:
        Logger configurado
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent.parent

    logs_dir = base_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("impar-automations")
    logger.setLevel(logging.DEBUG)

    # Handler para arquivo JSON (login_attempts.log)
    login_handler = logging.FileHandler(logs_dir / "login_attempts.log", encoding="utf-8")
    login_handler.setLevel(logging.INFO)
    login_formatter = JSONFormatter()
    login_handler.setFormatter(login_formatter)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    logger.addHandler(login_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "impar-automations") -> logging.Logger:
    """Obtém logger configurado"""
    return logging.getLogger(name)
