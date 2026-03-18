import json
import unicodedata
from sys_insert import inserir_sistema

def main():

    # Salvando o input (cardápio)
    with open('input.json', 'r', encoding='utf-8') as arquivo_input:
        cardapio = json.load(arquivo_input)

    # Salvando o database
    with open('database.json', 'r', encoding='utf-8') as arquivo_database:
        banco = json.load(arquivo_database) 

    cardapio_atualizado = insercao_imagens(cardapio, banco) 
    salvar_json(cardapio_atualizado)

    
def normalizar_texto(texto):
    if not texto:
        return ""

    # Deixa tudo minúsculo e tira espaços das pontas
    texto = texto.lower().strip()

    texto_sem_acento = ''.join(
        letra for letra in unicodedata.normalize('NFD', texto)
        if unicodedata.category(letra) != 'Mn'
    )


    return texto_sem_acento


def insercao_imagens(cardapio, banco):

    # Verifica se é uma ou mais categorias (coloca [])

    if isinstance(cardapio, dict):
        lista_categorias = [cardapio]
    else:
        lista_categorias = cardapio

    #Loop principal pelo cardápio

    for categoria in lista_categorias:
        if 'products' in categoria:
            
            for produto in (categoria['products']):

                nome_atual = produto['name']
                nome_limpo = normalizar_texto(nome_atual)

                imagem_encontrada = ""

                # Entra nas categorias do banco (bebidas, cervejas ...)

                for categoria_banco, produtos_da_categoria in banco.items():

                    if categoria_banco == 'regras':
                        continue

                    # Passar pelos produtos dentro das categorias do banco

                    for produto_banco, dados_produto_banco in produtos_da_categoria.items():
                        if nome_limpo == produto_banco or nome_limpo in dados_produto_banco.get('aliases', []):
                            imagem_encontrada = dados_produto_banco['image']
                            break
                    
                    if imagem_encontrada:
                        break

                if imagem_encontrada:
                    produto['image'] = imagem_encontrada

                
                # Logica para colocar imagens nos complementos do produto
                
                if 'complements' in produto:
                    
                    for grupo_complemento in produto['complements']:
                        if 'items' in grupo_complemento:

                            for item in grupo_complemento['items']:
                                imagem_encontrada_item = ""
                                nome_item = item['name']
                                nome_item_limpo = normalizar_texto(nome_item)

                                for categoria_banco, items_da_categoria in banco.items():

                                    if categoria_banco == 'regras':
                                        continue

                                    # Passar pelos items dentro das categorias do banco

                                    for item_banco, dados_item_banco in items_da_categoria.items():
                                        if nome_item_limpo == item_banco or nome_item_limpo in dados_item_banco.get('aliases', []):
                                            imagem_encontrada_item = dados_item_banco['image']
                                            break
                                    
                                    if imagem_encontrada_item:
                                        break

                                if imagem_encontrada_item:
                                    item['image'] = imagem_encontrada_item
    return cardapio

def salvar_json(cardapio_atualizado):

    with open("output.json", 'w', encoding='utf-8') as arquivo_saida:
        json.dump(cardapio_atualizado, arquivo_saida, ensure_ascii=False, indent=4)

    print("Arquivo local salvo em output.json")

    inserir_sistema()

if __name__ == "__main__":
    main()
