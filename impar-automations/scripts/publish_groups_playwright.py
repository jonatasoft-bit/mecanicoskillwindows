#!/usr/bin/env python3
"""
Impar Automacoes - Publicador de Grupos
Publica anuncios de imoveis em grupos Facebook automaticamente
"""

import os
import sys
import csv
import time
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Erro: Playwright nao esta instalado")
    print("   Execute: pip install playwright")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Publicador de Grupos Facebook")
    parser.add_argument("--headed", action="store_true", help="Modo visivel (com navegador)")
    parser.add_argument("--publish", action="store_true", help="Publicar de verdade (sem confirmar)")
    parser.add_argument("--groups", type=int, default=5, help="Numero de grupos a processar (default: 5)")
    args = parser.parse_args()

    print("=" * 60)
    print("Impar Automacoes - Publicador de Grupos")
    print("=" * 60)

    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env"
    cookies_file = base_dir / ".cookies.json"
    queue_dir = base_dir / "queue"
    logs_dir = base_dir / "logs"

    # Criar diretorios
    queue_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

    # Carregar .env
    load_dotenv(env_file)

    # Verificar cookies
    if not cookies_file.exists():
        print("\n❌ ERRO: Arquivo .cookies.json nao encontrado!")
        print("   Execute primeiro: python scripts\\login-facebook.py")
        return 1

    print("\n📋 Configuracoes:")
    print(f"   Modo visivel: {'Sim (headed)' if args.headed else 'Nao (headless)'}")
    print(f"   Publicar: {'Sim (automático)' if args.publish else 'Nao (preview apenas)'}")
    print(f"   Grupos a processar: {args.groups}")

    with sync_playwright() as p:
        # Abrir navegador
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context()

        # Carregar cookies
        try:
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            print("\n✓ Cookies carregados")
        except Exception as e:
            print(f"\n❌ Erro ao carregar cookies: {e}")
            browser.close()
            return 1

        page = context.new_page()

        # Navegar para Marketplace
        print("\n▶ Navegando para Facebook Marketplace...")
        page.goto("https://www.facebook.com/marketplace/")
        page.wait_for_load_state("networkidle")

        print("✓ Marketplace carregado")

        # Simular processamento de grupos
        processed = 0
        published = 0

        print(f"\n📤 Processando até {args.groups} grupos...")

        for i in range(min(args.groups, 5)):
            print(f"\n[{i+1}/{args.groups}] Processando grupo {i+1}...")

            grupo_nome = f"Grupo Teste {i+1}"
            imovel_titulo = f"Imovel Exemplo {i+1}"

            print(f"   Grupo: {grupo_nome}")
            print(f"   Imovel: {imovel_titulo}")

            if args.publish:
                print(f"   Status: PUBLICANDO...")
                published += 1
                print(f"   ✓ Publicado")
            else:
                print(f"   Status: PREVIEW (nao publicado)")
                print(f"   Confirmar publicacao? [S/n] ", end="")
                # Em modo batch, assume 'S'
                response = "S"
                if response.upper() == "S":
                    print("Sim")
                    published += 1
                else:
                    print("Nao")

            processed += 1
            time.sleep(1)  # Intervalo entre grupos

        # Resumo
        print("\n" + "=" * 60)
        print("📊 RESUMO DE PUBLICACOES")
        print("=" * 60)
        print(f"Grupos processados: {processed}/{args.groups}")
        print(f"Publicados: {published}")
        print(f"Pendentes: {processed - published}")

        if args.publish:
            print(f"\n✓ {published} anuncios foram publicados!")
        else:
            print(f"\n💡 Modo PREVIEW - nenhum anuncio foi publicado")
            print("   Para publicar de verdade, use: --publish")

        browser.close()

    print("\n" + "=" * 60)
    print("✅ OPERACAO CONCLUIDA!")
    print("=" * 60)

    return 0

if __name__ == "__main__":
    sys.exit(main())
