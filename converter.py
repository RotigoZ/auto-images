import json

def main():

    # Salvando o input (cardápio)
    with open('input.json', 'r', encoding='utf-8') as arquivo_input:
        cardapio = json.load(arquivo_input)

    # Salvando o database
    with open('database.json', 'r', encoding='utf-8') as arquivo_database:
        banco = json.load(arquivo_database)


if __name__ == "__main__":
    main()