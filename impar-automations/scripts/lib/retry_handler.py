#!/usr/bin/env python3
"""
Manipulador de Retry com Backoff Exponencial
Implementa retry com backoff: 2s, 4s, 8s, 16s, 32s
"""

import time
from typing import Callable, Any, List


class RetryHandler:
    """Gerencia retry com backoff exponencial"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: int = 2,
        backoff_multiplier: int = 2,
        max_delay: int = 32
    ):
        """
        Inicializa retry handler

        Args:
            max_attempts: Número máximo de tentativas (padrão: 3)
            initial_delay: Delay inicial em segundos (padrão: 2)
            backoff_multiplier: Multiplicador de backoff (padrão: 2)
            max_delay: Delay máximo em segundos (padrão: 32)
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.backoff_multiplier = backoff_multiplier
        self.max_delay = max_delay
        self.attempts = 0
        self.last_error = None

    def execute(
        self,
        func: Callable,
        *args,
        on_error: Callable = None,
        **kwargs
    ) -> Any:
        """
        Executa função com retry automático

        Args:
            func: Função a executar
            args: Argumentos posicionais
            on_error: Callback para erro (recebe tentativa, erro, delay)
            kwargs: Argumentos nomeados

        Returns:
            Resultado da função
        """
        self.attempts = 0
        delay = self.initial_delay

        for attempt in range(1, self.max_attempts + 1):
            self.attempts = attempt
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.last_error = e

                if attempt < self.max_attempts:
                    if on_error:
                        on_error(attempt, e, delay)
                    time.sleep(delay)
                    delay = min(delay * self.backoff_multiplier, self.max_delay)
                else:
                    if on_error:
                        on_error(attempt, e, 0)
                    raise

        return None

    def get_status(self) -> dict:
        """Retorna status das tentativas"""
        return {
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "last_error": str(self.last_error) if self.last_error else None,
            "success": self.last_error is None
        }


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: int = 2
) -> Callable:
    """
    Decorator para retry automático com backoff

    Args:
        max_attempts: Máximo de tentativas
        initial_delay: Delay inicial

    Returns:
        Função decorada
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            handler = RetryHandler(
                max_attempts=max_attempts,
                initial_delay=initial_delay
            )

            def on_error(attempt, error, delay):
                print(f"⚠ Tentativa {attempt} falhou: {error}")
                if delay > 0:
                    print(f"  Aguardando {delay}s antes da próxima tentativa...")

            return handler.execute(func, *args, on_error=on_error, **kwargs)

        return wrapper
    return decorator
