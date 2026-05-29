import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

# جلب توكن البوت المخزن في متغيرات البيئة على Render
TOKEN = os.getenv("BOT_TOKEN")

# دالة التعامل مع رسائل تيليجرام الأعمال (Telegram Business)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)  # لطباعة البيانات في الـ Logs لمراقبة العمل
    
    if update.business_message:  
        msg = update.business_message  
        user_text = msg.text  
        
        # نص الرد التلقائي
        reply = f"وصلت رسالتك:\n{user_text}"  
        
        # إرسال الرد عبر اتصال الأعمال الخاص بالملف الشخصي
        await context.bot.send_message(  
            chat_id=msg.chat.id,  
            text=reply,  
            business_connection_id=msg.business_connection_id  
        )

# بناء تطبيق البوت
app = Application.builder().token(TOKEN).build()

# إضافة استقبال لجميع أنواع الرسائل
app.add_handler(
    MessageHandler(filters.ALL, handle_message)
)

# تحديد المنفذ الخاص بالسيرفر
PORT = int(os.environ.get("PORT", 8443))

# تهيئة حلقة الأحداث (Event Loop) يدوياً لحل مشكلة التوافقية مع Python 3.14+
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# تشغيل البوت عبر تقنية Webhook المناسبة للسيرفرات المجانية
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url="https://tjroba-1.onrender.com",
    secret_token="MySecretToken123"
)
