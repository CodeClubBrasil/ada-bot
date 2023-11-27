import pytest
from unittest.mock import AsyncMock, MagicMock
from commands import handle_commands


@pytest.mark.asyncio
async def test_handle_commands_buscarclubes():
    # Configuração do mock
    message = MagicMock()
    message.author = MagicMock()
    message.content = "@Ada !buscarclubes Ri"
    message.channel = AsyncMock()

    bot = MagicMock()
    bot.user = MagicMock()

    # Simular a chamada da função handle_commands
    await handle_commands(bot, message)

    # Verifica se message.channel.send foi chamado com uma mensagem específica
    mensagem_esperada = "Não foi possível obter a lista de clubes para a cidade Ri."
    message.channel.send.assert_called_with(mensagem_esperada)
