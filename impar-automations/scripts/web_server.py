#!/usr/bin/env python3
"""
Servidor Web - Dashboard de Automação Facebook
Fornece interface visual para login e monitoramento
"""

import os
import sys
import webbrowser
from pathlib import Path
from flask import Flask, jsonify, render_template, send_from_directory

sys.path.insert(0, str(Path(__file__).parent / "lib"))

from lib.web_api import AutomationAPI
from lib.logger_config import setup_logging

# Inicializar logging
setup_logging()

# Criar aplicação Flask
app = Flask(__name__, template_folder="../web", static_folder="../web/static")
base_dir = Path(__file__).parent.parent

# Inicializar API
api = AutomationAPI(base_dir)


@app.route("/")
def index():
    """Página inicial do dashboard"""
    return render_template("index.html")


@app.route("/login.html")
def login_page():
    """Página de login"""
    return render_template("login.html")


# API Routes
@app.route("/api/status", methods=["GET"])
def api_status():
    """GET /api/status - Obtém status atual"""
    return jsonify(api.get_status())


@app.route("/api/history", methods=["GET"])
def api_history():
    """GET /api/history - Obtém histórico de tentativas"""
    return jsonify(api.get_history())


@app.route("/api/login", methods=["POST"])
def api_login():
    """POST /api/login - Inicia login interativo"""
    return jsonify(api.start_interactive_login())


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """POST /api/refresh - Tenta refresh automático"""
    return jsonify(api.refresh_cookies_now())


@app.route("/api/setup-scheduler", methods=["GET"])
def api_setup_scheduler():
    """GET /api/setup-scheduler - Configura Task Scheduler"""
    return jsonify(api.setup_scheduler())


@app.route("/api/notifications", methods=["GET"])
def api_notifications():
    """GET /api/notifications - Obtém notificações"""
    return jsonify(api.get_notifications())


@app.route("/static/<path:path>")
def serve_static(path):
    """Serve arquivos estáticos"""
    return send_from_directory(app.static_folder, path)


def open_browser():
    """Abre navegador automaticamente"""
    import threading
    import time

    def browser_thread():
        time.sleep(1)
        webbrowser.open("http://localhost:5000")

    thread = threading.Thread(target=browser_thread, daemon=True)
    thread.start()


def main():
    """Inicia o servidor web"""
    print("=" * 70)
    print("Impar Automations - Dashboard Web")
    print("=" * 70)

    print("\n🌐 Iniciando servidor web...")
    print("   Endereço: http://localhost:5000")
    print("   Navegador: Abrindo automaticamente em 1 segundo...")
    print("\n⏹️  Para parar: Pressione Ctrl+C\n")

    # Abrir navegador
    open_browser()

    # Iniciar servidor
    try:
        app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\n👋 Servidor encerrado")
        sys.exit(0)


if __name__ == "__main__":
    main()
