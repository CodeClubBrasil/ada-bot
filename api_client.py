import requests
import discord


def formatar_clube(clube):
    nome_clube = clube['name']
    bairro = clube['venue']['address']['address_2']
    cidade = clube['venue']['address']['city']
    estado = clube['venue']['address']['region']
    nome_lider = clube['contact']['name']

    embed = discord.Embed(
        title=nome_clube,
        colour=discord.Colour.green()
    )
    embed.add_field(name="Cidade", value=cidade, inline=True)
    embed.add_field(name="Estado", value=estado, inline=True)
    embed.add_field(name="Responsável:", value=nome_lider, inline=True)

    return embed


def buscar_clubes_ccw(bearer_token, country_code='BR', estado='active', cidade=None, max_pages=10):
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
                cidade_normalizada = cidade.lower()
                # Adicionar clubes filtrados por cidade à lista
                clubes.extend([clube for clube in dados_clubes if clube['venue']['address']['city'].lower() == cidade_normalizada])
            else:
                # Adicionar todos os clubes à lista
                clubes.extend(dados_clubes)
        else:
            print(f"Erro na página {pageNumber}: {response.status_code}")
            break

    return clubes
