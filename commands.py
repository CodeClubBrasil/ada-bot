import asyncio
from api_client import buscar_clubes_ccw
from utils import dividir_mensagens
from config import CCW_API_KEY


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
