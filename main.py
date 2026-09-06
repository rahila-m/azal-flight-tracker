import time
from apscheduler.schedulers.background import BackgroundScheduler
from src.database.db import init_db
from src.config import DEFAULT_ROUTES
from src.scraper.azal_scraper import fetch_azal_flight_price
from src.services.tracker_service import process_flight_check

def run_price_check():
    """Tüm aktif rotaları sırayla kontrol eder."""
    print("\n" + "="*50)
    print("🕒 Fiyat Kontrol Döngüsü Başlatıldı...")
    print("="*50)

    for route in DEFAULT_ROUTES:
        flight_data = fetch_azal_flight_price(
            origin=route["origin"],
            destination=route["destination"],
            departure_date=route["date"],
            headless=True
        )

        if flight_data and flight_data.get("price"):
            process_flight_check(
                origin=flight_data["origin"],
                destination=flight_data["destination"],
                departure_date=flight_data["departure_date"],
                current_price=flight_data["price"],
                currency=flight_data.get("currency", "AZN")
            )
        else:
            print(f"[Hata] {route['origin']} -> {route['destination']} için fiyat alınamadı.")

    print("\n✅ Kontrol tamamlandı. Bir sonraki kontrol planlandı.\n")

if __name__ == "__main__":
    print("🚀 AZAL Fiyat Takipçisi Başlatılıyor...")
    
    # 1. Veritabanını hazırla
    init_db()

    # 2. İlk kontrolü program açılır açılmaz anında yap
    run_price_check()

    # 3. Her 1 saatte bir çalışacak zamanlayıcıyı başlat
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_price_check, 'interval', hours=1)
    scheduler.start()

    print("⏳ Zamanlayıcı aktif: Sistem her 1 saatte bir fiyatları kontrol edecek.")
    print("Programı kapatmak için konsolda Ctrl + C tuşlarına basabilirsiniz.\n")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\nSistem kapatıldı.")
