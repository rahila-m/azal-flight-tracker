from src.database.repository import get_or_create_route, get_latest_price, save_price
from src.services.telegram_bot import send_telegram_message, format_price_drop_message

def process_flight_check(origin: str, destination: str, departure_date: str, current_price: float, currency: str = "AZN"):
    """
    1. Veritabanından rotayı bulur veya açar.
    2. Önceki fiyatla karşılaştırır.
    3. Fiyat düştüyse Telegram'a haber verir.
    4. Yeni fiyatı veritabanına kaydeder.
    """
    route_id = get_or_create_route(origin, destination, departure_date)
    previous_price = get_latest_price(route_id)

    print(f"\n--- [{origin} -> {destination}] Tarih: {departure_date} ---")
    print(f"Güncel Fiyat: {current_price} {currency}")

    if previous_price is None:
        print(f"Bilgi: Bu rota için ilk kayıt. Karşılaştırma için kaydediliyor.")
        save_price(route_id, current_price, currency)
        return

    print(f"Önceki Fiyat: {previous_price} {currency}")

    if current_price < previous_price:
        print(f"🔥 FİYAT DÜŞÜŞÜ TESPİT EDİLDİ: {previous_price} -> {current_price} {currency}")
        message = format_price_drop_message(
            origin=origin,
            destination=destination,
            date=departure_date,
            old_price=previous_price,
            new_price=current_price,
            currency=currency
        )
        send_telegram_message(message)
    elif current_price > previous_price:
        print(f"📈 Fiyat arttı (+{round(current_price - previous_price, 2)} {currency}). Bildirim gönderilmiyor.")
    else:
        print("Değişim yok: Fiyat aynı kaldı.")

    # Yeni fiyatı geçmişe kaydet
    save_price(route_id, current_price, currency)
