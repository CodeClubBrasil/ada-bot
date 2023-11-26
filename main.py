import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv
import asyncio
import requests

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CCW_API_KEY = os.getenv("CCW_API_KEY")

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = OPENAI_API_KEY


def formatar_clube(clube):
    nome_clube = clube['name']
    bairro = clube['venue']['address']['address_2']
    cidade = clube['venue']['address']['city']
    estado = clube['venue']['address']['region']
    nome_lider = clube['contact']['name']
    return f"{nome_clube} | {bairro} {cidade} {estado} | {nome_lider}"


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


def dividir_mensagens(clubes, limite=4000):
    mensagens = []
    mensagem_atual = ""
    for clube in clubes:
        if len(mensagem_atual) + len(clube) > limite:
            mensagens.append(mensagem_atual)
            mensagem_atual = clube
        else:
            mensagem_atual += clube + "\n"
    mensagens.append(mensagem_atual)
    return mensagens


async def buscar_historico_canal(canal, limit=7):
    historico = []

    async for message in canal.history(limit=limit, oldest_first=False):
        # Ignorar as mensagens recentes do próprio bot
        if message.author.id == bot.user.id:
            continue

        role = "user" if message.author.id != bot.user.id else "system"
        historico.append(f"{role}: {message.clean_content}")

    historico_formatado = "\n".join(historico)
    return historico_formatado


def ask_gpt(mensagens_formatadas):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usando um modelo de chat adequado
            messages=[{"role": "system", "content": mensagens_formatadas}],
            max_tokens=300,  # Definindo o limite máximo de tokens
            temperature=0.9  # Definindo a temperatura para a criatividade das respostas
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return "Desculpe, não consegui processar sua solicitação."


def dividir_resposta(resposta, limite=2000):
    """Divide a resposta em partes, cada uma com no máximo 'limite' caracteres."""
    partes = []
    while len(resposta) > 0:
        if len(resposta) > limite:
            ponto_quebra = resposta.rfind(" ", 0, limite)
            if ponto_quebra == -1:
                ponto_quebra = limite
            partes.append(resposta[:ponto_quebra])
            resposta = resposta[ponto_quebra:]
        else:
            partes.append(resposta)
            break
    return partes


@bot.event
async def on_ready():
    print(f"O {bot.user.name} ficou online!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Verificar se o bot foi mencionado e se o comando é !buscarclubes
    if bot.user in message.mentions and message.content.startswith('!buscarclubes'):
        async with message.channel.typing():
            # Extrair o nome da cidade do comando
            partes = message.content.split()
            cidade = partes[2] if len(partes) > 2 else None

            clubes = buscar_clubes_ccw(CCW_API_KEY, cidade=cidade)
            if clubes:
                partes = dividir_mensagens(clubes)
                for parte in partes:
                    await message.channel.send(parte)
            else:
                await message.channel.send(f"Não foi possível obter a lista de clubes para a cidade {cidade}.")
        return

    # Lógica para lidar com outras menções ao bot
    if bot.user in message.mentions:
        async with message.channel.typing():
            historico = await buscar_historico_canal(message.channel)
            mensagem_atual = f"user: {message.clean_content}"
            historico_com_mensagem_atual = historico + "\n" + mensagem_atual

            def responder():
                return ask_gpt(historico_com_mensagem_atual)

            resposta = await asyncio.get_event_loop().run_in_executor(None, responder)
            for parte in dividir_resposta(resposta):
                await message.channel.send(parte)
        return


bot.run(DISCORD_BOT_TOKEN)
