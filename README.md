# Auto Images

Script para adicionar imagens automaticamente em um cardapio digital.

## Como funciona

O script le um cardapio sem imagens (ou com imagens faltando), procura os produtos e complementos no banco de imagens, e gera um novo JSON pronto para importacao.

Fluxo:
1. Ler `input.json` (cardapio de entrada).
2. Ler `database.json` (base de imagens e aliases).
3. Procurar correspondencia por nome normalizado (minusculo, sem acento, sem espacos nas pontas).
4. Preencher `image` em produtos e complementos quando encontrar.
5. Salvar resultado em `output.json`.

## Divisao de arquivos

- `converter.py` -> Logica de conversao.
- `database.json` -> Local onde sao salvos os links das imagens dos produtos/complementos.
- `input.json` -> Local onde sao inseridas as categorias sem imagens.
- `output.json` -> Saida das categorias com imagens.

## Requisitos

- Python 3.8+ (recomendado)
- Nao precisa instalar bibliotecas externas (usa apenas bibliotecas padrao: `json` e `unicodedata`)

## Como usar

No terminal, dentro da pasta do projeto:

```bash
python converter.py
```

Se estiver usando o launcher do Windows:

```bash
py converter.py
```

Ao final, o script gera (ou sobrescreve) o arquivo `output.json`.

Mensagem esperada:

```text
Sucesso! O arquivo 'output.json' foi gerado e esta pronto para importacao.
```

## Estrutura esperada (resumo)

### `database.json`

Cada entrada de item no banco deve ter, no minimo:

- `image`: URL da imagem
- `aliases`: lista opcional com variacoes de nome para facilitar o match

Exemplo simplificado:

```json
{
  "hamburgueres": {
    "x-burger": {
      "image": "https://exemplo.com/x-burger.jpg",
      "aliases": ["x burger", "burger simples"]
    }
  },
  "regras": {}
}
```

### `input.json`

Pode ser:
- Um objeto de categoria unico, ou
- Uma lista de categorias

Cada categoria pode conter `products`, e cada produto pode conter `complements` com `items`.

## Observacoes

- A busca ignora diferencas de acentos e maiusculas/minusculas.
- Se nao encontrar imagem para um item, o campo `image` nao e adicionado para ele.
- O script ignora a chave `regras` dentro do `database.json`.
