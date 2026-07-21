#!/usr/bin/env python3
"""
Impar Automacoes - Enhancements com OpenAI
Melhora titulos e descricoes de imoveis usando IA
"""

import os
import sys
import csv
from pathlib import Path
from dotenv import load_dotenv

try:
    import openai
except ImportError:
    print("❌ Erro: openai nao esta instalado")
    print("   Execute: pip install openai")
    sys.exit(1)

def main():
    print("=" * 60)
    print("Impar Automacoes - Enhancements com OpenAI")
    print("=" * 60)

    base_dir = Path(__file__).parent.parent
    env_file = base_dir / ".env"
    data_dir = base_dir / "data"

    # Carregar .env
    load_dotenv(env_file)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ ERRO: OPENAI_API_KEY nao configurada no .env!")
        print("   Edite: impar-automations\.env")
        print("   Adicione: OPENAI_API_KEY=sk-...")
        return 1

    openai.api_key = api_key

    print("\n✓ OpenAI API configurada")
    print("📝 Processando imoveis...")

    # Carregar imoveis
    locacao_file = data_dir / "imoveis-locacao.csv"
    if not locacao_file.exists():
        print(f"\n❌ Arquivo nao encontrado: {locacao_file}")
        return 1

    print(f"\n▶ Lendo: {locacao_file.name}")

    imoveis = []
    with open(locacao_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        imoveis = list(reader)

    print(f"✓ {len(imoveis)} imoveis carregados")

    enhanced = []

    for i, imovel in enumerate(imoveis[:3], 1):  # Processar apenas os 3 primeiros (economiza API)
        print(f"\n[{i}/{min(3, len(imoveis))}] Processando: {imovel.get('titulo', 'Sem titulo')}")

        try:
            # Melhorar titulo
            titulo_prompt = f"""Melhore este titulo de anuncio imobiliario para ser mais atrativo em redes sociais.
Titulo original: {imovel.get('titulo', '')}
Quartos: {imovel.get('quartos', '?')}
Bairro: {imovel.get('endereco', '?')}

Retorne APENAS o novo titulo (uma linha)."""

            titulo_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": titulo_prompt}],
                temperature=0.7,
                max_tokens=50
            )

            novo_titulo = titulo_response['choices'][0]['message']['content'].strip()
            print(f"   Titulo original: {imovel.get('titulo')}")
            print(f"   Novo titulo: {novo_titulo}")

            # Melhorar descricao
            desc_prompt = f"""Melhore esta descricao de anuncio imobiliario. Seja conciso e atrativo.
Descricao original: {imovel.get('descricao', '')[:100]}...
Preco: R${imovel.get('preco', '?')}

Retorne APENAS a descricao melhorada (2-3 linhas)."""

            desc_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": desc_prompt}],
                temperature=0.7,
                max_tokens=100
            )

            nova_descricao = desc_response['choices'][0]['message']['content'].strip()
            print(f"   Descricao: {nova_descricao[:60]}...")

            # Salvar versao melhorada
            enhanced.append({
                'original_titulo': imovel.get('titulo'),
                'novo_titulo': novo_titulo,
                'original_descricao': imovel.get('descricao', '')[:100],
                'nova_descricao': nova_descricao,
                'preco': imovel.get('preco')
            })

        except Exception as e:
            print(f"   ⚠ Erro ao processar: {e}")
            continue

    # Salvar resultado
    if enhanced:
        output_file = base_dir / "queue" / "enhanced_listings.csv"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=enhanced[0].keys())
            writer.writeheader()
            writer.writerows(enhanced)

        print(f"\n✓ Resultados salvos em: {output_file.name}")

    print("\n" + "=" * 60)
    print("✅ ENHANCEMENT CONCLUIDO!")
    print("=" * 60)
    print(f"Processados: {len(enhanced)} imoveis")
    print("\n💡 Proximos passos:")
    print("   - Revisar as melhorias em: queue/enhanced_listings.csv")
    print("   - Usar os novos titulos e descricoes nos anuncios")

    return 0

if __name__ == "__main__":
    sys.exit(main())
