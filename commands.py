import asyncio
import discord
from discord.ext import commands
from api_client import buscar_clubes_ccw
from utils import dividir_mensagens
from chat_gpt import ask_gpt
from config import CCW_API_KEY

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)


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


async def handle_commands(bot, message):
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

    # Lógica para lidar com outras menções ao bot usando ChatGPT
    if bot.user in message.mentions and message.content.startswith('!duvida'):
        async with message.channel.typing():
            historico = await buscar_historico_canal(message.channel)
            mensagem_atual = f"user: {message.clean_content}"
            historico_com_mensagem_atual = historico + "\n" + mensagem_atual

            resposta = await ask_gpt(historico_com_mensagem_atual)
