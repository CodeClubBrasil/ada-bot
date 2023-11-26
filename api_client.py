import requests


def formatar_clube(clube):
    nome_clube = clube['name']
    bairro = clube['venue']['address']['address_2']
    cidade = clube['venue']['address']['city']
    estado = clube['venue']['address']['region']
    nome_lider = clube['contact']['name']
    return f"{nome_clube} | {bairro} {cidade} {estado} | {nome_lider}"


def buscar_clubes_ccw(bearer_token, country_code='BR', estado='active', cidade=None, max_pages=10):
    # ... [implementação da função buscar_clubes_ccw] ...
    clubes = []
    base_url = 'https://api.codeclubworld.org/clubs'

    for pageNumber in range(max_pages):
        url = f"{base_url}?page={pageNumber}&in_country={country_code}&state={estado}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados_clubes = response.json()
            if cidade:
                # Normaliza a cidade para comparação
                cidade_normalizada = cidade.lower()
                clubes_cidade = [formatar_clube(
                    clube) for clube in dados_clubes if clube['venue']['address']['city'].lower() == cidade_normalizada]
            else:
                clubes_cidade = [formatar_clube(clube)
                                 for clube in dados_clubes]
            clubes.extend(clubes_cidade)
        else:
            print(f"Erro na página {pageNumber}: {response.status_code}")
            break

    return clubes

