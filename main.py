import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import engine, Base
from config import settings
from bot.dispatcher import bot, dp, set_webhook, delete_webhook
from bot.handlers.start import router as start_router
from api.notes import router as notes_router
from api.channels import router as channels_router
from api.admin import router as admin_router
from web.routes import router as web_router
from aiogram.types import Update
import logging

logging.basicConfig(level=logging.INFO)

# إنشاء جداول قاعدة البيانات عند البداية
Base.metadata.create_all(bind=engine)

# تضمين معالجات البوت
dp.include_router(start_router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # بداية التشغيل: تعيين Webhook للبوت
    if settings.WEBHOOK_URL:
        await set_webhook()
        logging.info(f"Webhook set to {settings.WEBHOOK_URL}/webhook")
    else:
        logging.warning("WEBHOOK_URL غير مضبوط. البوت لن يستقبل تحديثات.")
    yield
    # إنهاء التشغيل: حذف Webhook
    await delete_webhook()

app = FastAPI(lifespan=lifespan)

# تضمين المسارات
app.include_router(web_router)
app.include_router(notes_router)
app.include_router(channels_router)
app.include_router(admin_router)

# خدمة الملفات الثابتة (CSS, JS, صور)
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# نقطة استقبال تحديثات تيليجرام
@app.post("/webhook")
async def telegram_webhook(update: Update):
    await dp.feed_webhook_update(bot, update)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
