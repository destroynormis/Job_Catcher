import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from pathlib import Path
from handlers import router  # Импортируем роутер из handlers.py

# Указываем путь к .env явно
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

with open(dotenv_path, "r", encoding="utf-8") as f:
    print(f"DEBUG: Читаю файл: {f.read()}")

# Загружаем переменные
TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


async def main() -> None:
    # Проверка ключей
    if not TOKEN:
        sys.exit("❌ Ошибка: BOT_TOKEN не найден в .env")
    if not GOOGLE_API_KEY:
        print("⚠️ Предупреждение: GOOGLE_API_KEY не найден!")

    # Инициализация
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    print("🚀 JobCatcher успешно запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен.")