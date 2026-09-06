import requests
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message: str) -> bool:
    """Telegram botu üzerinden kullanıcıya mesaj gönderir."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Uyarı] Telegram token veya Chat ID tanımlı değil!")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"[Hata] Telegram mesajı gönderilemedi: {e}")
        return False

def format_price_drop_message(
    origin: str,
    destination: str,
    date: str,
    old_price: float,
    new_price: float,
    currency: str = "AZN"
) -> str:
    """Fiyat düşüşü için bildirim metni üretir."""
    diff = round(old_price - new_price, 2)
    percent = round((diff / old_price) * 100, 1)

    return (
        f"✈️ *AZAL Uçuş Fiyatı Düştü!*\n\n"
        f"📍 *Rota:* {origin} ➔ {destination}\n"
        f"📅 *Tarih:* {date}\n\n"
        f"💰 *Eski Fiyat:* {old_price} {currency}\n"
        f"🔥 *Yeni Fiyat:* {new_price} {currency}\n\n"
        f"📉 *Düşüş:* -{diff} {currency} (%{percent} indirim)"
    )

if __name__ == "__main__":
    test_msg = "🔔 *AZAL Takipçisi:* Test mesajı başarılı! Bot entegrasyonu tamamlandı."
    success = send_telegram_message(test_msg)
    print("Test mesaj sonucu:", "Başarılı ✅" if success else "Başarısız ❌")
