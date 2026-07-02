import hmac
import hashlib
import json
from urllib.parse import unquote, parse_qs
from typing import Optional
from config import settings


def verify_telegram_data(init_data: str) -> Optional[dict]:
    """
    يتحقق من صحة initData القادمة من تيليجرام.
    يعيد قاموس البيانات إذا كان التوقيع صحيحًا، وإلا None.
    """
    if not init_data:
        return None

    try:
        # فصل التوقيع عن البيانات
        parsed = parse_qs(init_data)
        received_hash = parsed.pop("hash", [None])[0]
        if not received_hash:
            return None

        # ترتيب المفاتيح أبجديًا وإعادة بناء سلسلة التحقق
        data_check_arr = []
        for key in sorted(parsed.keys()):
            values = parsed[key]
            for value in values:
                data_check_arr.append(f"{key}={value}")

        data_check_string = "\n".join(data_check_arr)

        # إنشاء المفتاح السري
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=settings.BOT_TOKEN.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # حساب التوقيع المحلي
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # مقارنة التوقيعين
        if not hmac.compare_digest(calculated_hash, received_hash):
            return None

        # فك ترميز JSON الموجود في user
        user_data = parsed.get("user", [None])[0]
        if user_data:
            user_dict = json.loads(unquote(user_data))
            return user_dict

        return None

    except Exception:
        return None


def get_user_id_from_init_data(init_data: str) -> Optional[int]:
    """
    يستخرج user_id من initData الموثقة.
    """
    user_data = verify_telegram_data(init_data)
    if user_data:
        return user_data.get("id")
    return None
