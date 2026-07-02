from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from config import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

async def set_webhook():
    if settings.WEBHOOK_URL:
        webhook_url = f"{settings.WEBHOOK_URL}/webhook"
        await bot.set_webhook(webhook_url)

async def delete_webhook():
    await bot.delete_webhook()

async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="فتح المنصة"),
    ]
    await bot.set_my_commands(commands)
