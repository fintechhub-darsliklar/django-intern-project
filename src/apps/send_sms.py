import requests

def send_telegram_otp(phone, otp):
    # Bu yerda o'zingizning Bot Token va Chat ID laringizni ishlating
    token = "SIZNING_BOT_TOKENINGIZ"
    chat_id = "SIZNING_CHAT_IDINGIZ" # Yoki foydalanuvchi chat_id'si
    text = f"Transfer tasdiqlash kodi: {otp}\nTelefon: {phone}"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    try:
        requests.get(url)
        return True
    except:
        return False