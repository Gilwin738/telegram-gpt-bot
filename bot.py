import os
import requests
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
import asyncio

# Токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Инициализация бота и роутера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
router = Router()

# Функция запроса к Together AI
async def chat_with_gpt(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": "Ты умный чат-бот."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    print("Статус код:", response.status_code)
    print("Ответ API:", response.text)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Ошибка API: {response.status_code} - {response.text}"

# Обработчик сообщений
@router.message()
async def handle_message(message: Message):
    response_text = await chat_with_gpt(message.text)
    await message.reply(response_text)

# Запуск бота
async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
