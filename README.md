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
- `sys_insert.py` -> Funcao para inserir no sistema as categorias do `output.json`.
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

## Envio direto para o sistema (`inserir_sistema`)

Agora o projeto tambem possui a funcao `inserir_sistema()` no arquivo `sys_insert.py`.

Ela autentica no sistema usando o usuario `suporte` e envia o conteudo do `output.json` para o endpoint de importacao de categorias.

Para funcionar, voce precisa:

1. Ter o arquivo `output.json` ja gerado.
2. Criar um arquivo `.env` na raiz do projeto com:

```env
SLUG_RESTAURANTE=seu_slug
SENHA=sua_senha
```

3. Instalar as dependencias necessarias para esse envio:

```bash
pip install requests python-dotenv
```

4. Chamar a funcao `inserir_sistema()` (por exemplo, em um script Python):

```python
from sys_insert import inserir_sistema

inserir_sistema()
```

Se `SLUG_RESTAURANTE` ou `SENHA` nao estiverem preenchidos, o envio nao sera executado.
