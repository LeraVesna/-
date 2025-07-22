import logging
import openai
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

openai.api_key = OPENAI_API_KEY

@dp.message_handler()
async def chat_with_gpt(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": message.text}],
            temperature=0.7,
            max_tokens=150
        )
        reply_text = response.choices[0].message.content
        await message.answer(reply_text)
    except Exception as e:
        logging.error(e)
        await message.answer("Что-то пошло не так. Попробуй позже.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)