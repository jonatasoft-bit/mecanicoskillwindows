#!/usr/bin/env python3
"""
Impar Automacoes - Gerar Fila Marketplace
Processa imoveis e gera fila para publicacao no marketplace
"""

import os
import sys
import csv
from datetime import datetime
from pathlib import Path

def main():
    print("=" * 50)
    print("Impar Automacoes - Gerador de Fila Marketplace")
    print("=" * 50)

    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    queue_dir = base_dir / "queue"

    # Verificar se diretorios existem
    if not data_dir.exists():
        print(f"❌ Erro: Diretorio {data_dir} nao encontrado")
        return 1

    queue_dir.mkdir(exist_ok=True)

    # Verificar arquivos CSV
    locacao_file = data_dir / "imoveis-locacao.csv"
    venda_file = data_dir / "imoveis-venda.csv"

    imoveis_locacao = []
    imoveis_venda = []

    # Carregar imoveis para locacao
    if locacao_file.exists():
        try:
            with open(locacao_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                imoveis_locacao = list(reader)
            print(f"✓ Carregados {len(imoveis_locacao)} imoveis para locacao")
        except Exception as e:
            print(f"⚠ Erro ao ler imoveis-locacao.csv: {e}")
    else:
        print(f"⚠ Arquivo nao encontrado: {locacao_file}")

    # Carregar imoveis para venda
    if venda_file.exists():
        try:
            with open(venda_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                imoveis_venda = list(reader)
            print(f"✓ Carregados {len(imoveis_venda)} imoveis para venda")
        except Exception as e:
            print(f"⚠ Erro ao ler imoveis-venda.csv: {e}")
    else:
        print(f"⚠ Arquivo nao encontrado: {venda_file}")

    # Gerar fila
    total = len(imoveis_locacao) + len(imoveis_venda)

    if total == 0:
        print("\n⚠ Nenhum imovel carregado!")
        print("   Verifique se os arquivos CSV existem em: data/")
        return 1

    # Criar arquivo de saida
    output_file = queue_dir / f"marketplace_queue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tipo', 'titulo', 'preco', 'descricao', 'data'])

        for imovel in imoveis_locacao:
            writer.writerow([
                'locacao',
                imovel.get('titulo', 'Sem titulo'),
                imovel.get('preco', '0'),
                imovel.get('descricao', '')[:100],
                datetime.now().isoformat()
            ])

        for imovel in imoveis_venda:
            writer.writerow([
                'venda',
                imovel.get('titulo', 'Sem titulo'),
                imovel.get('preco', '0'),
                imovel.get('descricao', '')[:100],
                datetime.now().isoformat()
            ])

    print(f"\n✓ Fila marketplace gerada com sucesso!")
    print(f"   Total: {total} imoveis")
    print(f"   Arquivo: {output_file}")
    print(f"   Cadencia: 7-20 minutos (humanizado)")

    return 0

if __name__ == "__main__":
    sys.exit(main())
