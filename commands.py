import asyncio
import discord
import re
from discord.ext import commands
from api_client import buscar_clubes_ccw
from utils import dividir_mensagens
from chat_gpt import ask_gpt_async
from config import CCW_API_KEY


async def buscar_historico_canal(bot, canal, limit=7):
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

    print(f"COMMANDS Conteúdo da Mensagem: '{message.content}'")
    # print(f"COMMANDS Autor: {message.author.name}")
    # print(f"COMMANDS Canal: {message.channel.name}")

    # Usar expressão regular para remover a menção ao bot
    conteudo_limpo = re.sub(r'<@!?(\d+)>', '', message.content).strip()
    print(f"Conteúdo Limpo da Mensagem: '{conteudo_limpo}'")

    # Verificar se o comando é !buscarclubes
    if conteudo_limpo.startswith('!buscarclubes'):
        print("Comando !buscarclubes detectado")
        await processar_buscar_clubes(message)
        return

    # Verificar se o comando é !duvida
    elif conteudo_limpo.startswith('!duvida'):
        print("Comando !duvida detectado")
        await processar_duvida(bot, message)
        return


async def processar_buscar_clubes(message):
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


async def processar_duvida(bot, message):
    async with message.channel.typing():

        historico = await buscar_historico_canal(bot, message.channel)
        mensagem_atual = f"user: {message.clean_content}"
        historico_com_mensagem_atual = historico + "\n" + mensagem_atual

        # Assumindo que ask_gpt é assíncrona
        resposta = await ask_gpt_async(historico_com_mensagem_atual)
        partes_resposta = dividir_mensagens(
            [resposta])  # Dividir a resposta
        for parte in partes_resposta:
            await message.channel.send(parte)
    return
