#!/usr/bin/env python3
"""
Impar Automacoes - Gerar Fila de Grupos
Processa 96 grupos e gera fila para publicacao
"""

import os
import sys
import csv
from datetime import datetime
from pathlib import Path

def main():
    print("=" * 50)
    print("Impar Automacoes - Gerador de Fila Grupos")
    print("=" * 50)

    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"
    queue_dir = base_dir / "queue"

    # Verificar diretorios
    if not data_dir.exists():
        print(f"❌ Erro: Diretorio {data_dir} nao encontrado")
        return 1

    queue_dir.mkdir(exist_ok=True)

    # Carregar grupos aprovados
    grupos_file = data_dir / "grupos-aprovados.csv"
    grupos = []

    if grupos_file.exists():
        try:
            with open(grupos_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                grupos = list(reader)
            print(f"✓ Carregados {len(grupos)} grupos aprovados")
        except Exception as e:
            print(f"⚠ Erro ao ler grupos-aprovados.csv: {e}")
    else:
        print(f"⚠ Arquivo nao encontrado: {grupos_file}")
        return 1

    if len(grupos) == 0:
        print("\n❌ Nenhum grupo carregado!")
        print("   Verifique o arquivo: data/grupos-aprovados.csv")
        return 1

    # Carregar imoveis
    locacao_file = data_dir / "imoveis-locacao.csv"
    venda_file = data_dir / "imoveis-venda.csv"

    imoveis = []

    if locacao_file.exists():
        with open(locacao_file, 'r', encoding='utf-8') as f:
            imoveis.extend(csv.DictReader(f))

    if venda_file.exists():
        with open(venda_file, 'r', encoding='utf-8') as f:
            imoveis.extend(csv.DictReader(f))

    print(f"✓ Carregados {len(imoveis)} imoveis")

    if len(imoveis) == 0:
        print("\n⚠ Nenhum imovel carregado!")
        return 1

    # Gerar fila de grupos
    output_file = queue_dir / f"groups_queue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['grupo_id', 'grupo_url', 'imovel_titulo', 'horario', 'status', 'data'])

        for idx, grupo in enumerate(grupos):
            imovel = imoveis[idx % len(imoveis)]  # Rodar imoveis

            horarios = ['11:30', '17:00', '21:30']
            horario = horarios[idx % 3]

            writer.writerow([
                grupo.get('grupo_id', ''),
                grupo.get('url', ''),
                imovel.get('titulo', 'Sem titulo'),
                horario,
                'pendente',
                datetime.now().isoformat()
            ])

    print(f"\n✓ Fila de grupos gerada com sucesso!")
    print(f"   Total: {len(grupos)} grupos")
    print(f"   Imoveis: {len(imoveis)}")
    print(f"   Arquivo: {output_file}")
    print(f"   Horarios: 11:30, 17:00, 21:30")
    print(f"   Limite: 30 grupos/dia (restricao Facebook)")

    return 0

if __name__ == "__main__":
    sys.exit(main())
