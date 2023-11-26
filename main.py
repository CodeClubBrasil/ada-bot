import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN
from commands import handle_commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.event
async def on_ready():
    print(f"O {bot.user.name} ficou online!")


@bot.event
async def on_message(message):
    await handle_commands(bot, message)

bot.run(DISCORD_BOT_TOKEN)
