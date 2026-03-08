import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from config import BOT_TOKEN
from bot.handlers import base, search

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(base.router)
dp.include_router(search.router)

async def on_startup(bot: Bot):
    logging.info("Бот готов к работе!")

dp.startup.register(on_startup)

app = web.Application()
webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
webhook_requests_handler.register(app, path="/webhook")
setup_application(app, dp, bot=bot)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Это главная точка входа для облака
    web.run_app(app, port=port)