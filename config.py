import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

if not all([TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, NOTION_API_KEY, NOTION_DATABASE_ID]):
    print("WARNING: Bazı ortam değişkenleri (.env) eksik. Lütfen yapılandırmanızı kontrol edin.")
