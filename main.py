import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

# 1. Загружаем секреты из файла .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    sys.exit("Ошибка: Токен не найден! Проверь файл .env")

# 2. Создаем диспетчер
dp = Dispatcher()

# 3. Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Бот отвечает пользователю, выделяя имя жирным шрифтом
    user_name = html.bold(message.from_user.full_name)
    await message.answer(f"Привет, {user_name}! Я твой личный бот для поиска вакансий. Готов к работе 🚀")

# 4. Главная функция запуска
async def main() -> None:
    # Инициализируем бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    print("Бот успешно запущен и слушает Telegram...")
    # Запускаем постоянный опрос серверов Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Включаем логирование
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")