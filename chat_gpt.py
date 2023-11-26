import asyncio
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def ask_gpt_async(mensagens_formatadas):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, ask_gpt_sync, mensagens_formatadas)

def ask_gpt_sync(mensagens_formatadas):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": mensagens_formatadas}],
            max_tokens=300,
            temperature=0.9
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return "Desculpe, não consegui processar sua solicitação."