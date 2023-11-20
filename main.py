import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = OPENAI_API_KEY


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

    if bot.user in message.mentions:
        async with message.channel.typing():
            historico = await buscar_historico_canal(message.channel)
            mensagem_atual = f"user: {message.clean_content}"
            historico_com_mensagem_atual = historico + "\n" + mensagem_atual

            def responder():
                return ask_gpt(historico_com_mensagem_atual)

            resposta = await asyncio.get_event_loop().run_in_executor(None, responder)
            # Dividir a resposta se necessário e enviar cada parte
            for parte in dividir_resposta(resposta):
                await message.channel.send(parte)


bot.run(DISCORD_BOT_TOKEN)
