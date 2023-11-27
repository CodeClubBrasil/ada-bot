import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from commands import handle_commands

# Configurar intents para incluir mensagens de guilda
intents = discord.Intents.default()
intents.messages = True  # Ativar intents de mensagens
intents.guild_messages = True  # Ativar intents de mensagens de guilda

# Criar bot com os intents configurados
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"A {bot.user.name} ficou online!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await handle_commands(bot, message)
    # Adicionando esta linha para processar comandos registrados
    await bot.process_commands(message)

bot.run(DISCORD_BOT_TOKEN)
