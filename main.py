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


@bot.event
async def on_ready():
    print(f"O {bot.user.name} ficou online!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    historico = await buscar_historico_canal(message.channel)
    mensagem_atual = f"user: {message.clean_content}"
    historico_com_mensagem_atual = historico + "\n" + mensagem_atual

    def responder():
        return ask_gpt(historico_com_mensagem_atual)

    async with message.channel.typing():
        resposta = await asyncio.get_event_loop().run_in_executor(None, responder)
        await message.channel.send(resposta)


bot.run(DISCORD_BOT_TOKEN)
