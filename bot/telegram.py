import requests

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_notification(text) -> bool:
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={text}"
        results = requests.get(url)
        print(results.json())
    except:
        return False
    return True
