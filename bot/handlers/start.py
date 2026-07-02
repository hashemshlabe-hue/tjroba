from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """ترسل رسالة ترحيبية مع زر فتح المنصة"""
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🕌 افتح المنصة",
                    web_app=WebAppInfo(url="https://your-domain.com")
                )
            ]
        ]
    )
    
    welcome_text = (
        "السلام عليكم ورحمة الله وبركاته 🕌\n\n"
        "مرحباً بك في منصة الإمام مالك التعليمية 📚\n\n"
        "المنصة تجمع لك:\n"
        "• جميع قنوات الكلية الرسمية\n"
        "• القنوات الدعوية والقرآنية\n"
        "• المجموعات الطلابية\n"
        "• كناشة المتفقه لتدوين الفوائد 📝\n\n"
        "اضغط الزر أدناه للدخول إلى المنصة 👇"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=keyboard
    )
