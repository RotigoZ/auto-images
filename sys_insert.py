import requests
from dotenv import load_dotenv
import os
import json

# Lógica para inserir as categorias com imagens direto no sistema
def inserir_sistema():
    load_dotenv()
    slug = os.getenv("SLUG_RESTAURANTE") 
    senha = os.getenv("SENHA")

    if not slug or not senha:
        print("Slug ou senha não foram fornecidos! Caso queira enviar direto para o sistema, preencha essas informações no arquivo .env")
        return
    
    r = requests.post(f'https://{slug}.stbl.com.br/core/v2/terminal/auth/start/', data={'username': 'suporte', 'password': {senha}})

    if r.status_code == 200:
        data = r.json()
        bearer = data['auth_token']
        print("Token encontrado!")
    else:
        print("Autenticação falhou: verifique as credenciais.")
        return
    
    with open('output.json', 'r', encoding='utf-8') as output_json:
        output_json = json.load(output_json)

        headers = {
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {bearer}",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "referrer": f"https://{slug}.suitable.app.br/",
        "referrerPolicy": "strict-origin-when-cross-origin",
    }
    
    p = requests.post(
    f'https://{slug}.stbl.com.br/estoque/v2/categories/import/?format=json', 
    headers=headers,
    json=output_json
)
    
    if p.status_code == 200:
        print(f"Categorias inseridas com sucesso no sistema {slug}!")
    elif p.status_code != 200:
        print(f"Erro ao inserir as categorias no sistema, verifique o json")
        erro = p.json()
        print(erro)