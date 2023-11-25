import requests
import os
from dotenv import load_dotenv

load_dotenv()

CCW_API_KEY = os.getenv("CCW_API_KEY")


def buscar_clubes_ccw(api_token, country_code='BR', max_pages=10):
    clubes = []
    base_url = "https://api.codeclubworld.org/clubs"

    for pageNumber in range(max_pages):
        url = f"{base_url}?page={pageNumber}&in_country={country_code}"
        headers = {
            'Authorization': api_token
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Adicione os clubes da página atual à lista total
            clubes.extend(response.json())
        else:
            print(f"Erro na página {pageNumber}: {response.status_code}")
            break  # Para de fazer requisições se encontrar um erro

    return clubes

# Para testar a função


def main():
    api_token = CCW_API_KEY  # Substitua pelo seu token real
    clubes = buscar_clubes_ccw(api_token)
    for clube in clubes:
        print(clube)  # Ajuste conforme a estrutura da resposta JSON


if __name__ == "__main__":
    main()
