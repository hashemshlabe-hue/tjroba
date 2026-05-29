from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print(update)

    if update.business_message:

        msg = update.business_message

        user_text = msg.text

        reply = f"وصلت رسالتك:\n{user_text}"

        await context.bot.send_message(
            chat_id=msg.chat.id,
            text=reply,
            business_connection_id=msg.business_connection_id
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.ALL, handle_message)
)

PORT = int(os.environ.get("PORT", 8443))

# تعديل السطر ليتناسب مع خوادم ريندر عبر استقبال الاتصالات على المنفذ الصحيح
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url="https://tjroba-1.onrender.com",
    secret_token="MySecretToken123"
)
