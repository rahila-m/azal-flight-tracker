import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

DEFAULT_ROUTES = [
    {"origin": "GYD", "destination": "ADB", "date": "2026-10-20", "target_price": 230.0},
    {"origin": "ADB", "destination": "GYD", "date": "2026-10-25", "target_price": 200.0},
]
