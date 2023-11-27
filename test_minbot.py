import discord
from discord.ext import commands

TOKEN = ''  

intents = discord.Intents.default()
intents.messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"Mensagem de {message.author}: {message.content}")

bot.run(TOKEN)