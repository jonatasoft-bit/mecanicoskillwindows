# Data - Imoveis e Configuracoes

Este diretorio contem:

## CSVs de Dados (Extrair do ZIP)

- **grupos-aprovados.csv** - 96 grupos Facebook aprovados para publicacao
- **imoveis-locacao.csv** - Base de imoveis para locacao
- **imoveis-venda.csv** - Base de imoveis para venda

Formato esperado:
- Encoding: UTF-8
- Delimitador: `,` (virgula)
- Com header (primeira linha = nomes das colunas)

## Configuracao

- **.env.template** - Template de configuracao (copie para .env)
- **.env** - Arquivo de configuracao (criado automaticamente, nao commite!)

## Como Adicionar

1. Extraia o arquivo ZIP
2. Copie os 3 CSVs do diretorio `data/` para este diretorio
3. Verifique que tem UTF-8 encoding (sem BOM)
4. O instalador validara automaticamente

## Estrutura dos CSVs

### grupos-aprovados.csv
```
url,grupo_id,nome,membros
https://www.facebook.com/groups/12345,12345,Nome do Grupo,5000
...
```

### imoveis-locacao.csv e imoveis-venda.csv
```
titulo,descricao,preco,endereco,quartos,banheiros,area,imagem_url
Casa 3 quartos em SP,Bela casa proxima...,3000.00,Rua X,3,2,120,...
...
```

Veja os CSVs originais no ZIP para formato exato.
