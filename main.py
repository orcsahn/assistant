import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import config
from bot.handlers import start, handle_message
from bot.jobs import daily_water_reminder, daily_sport_reminder

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    if not config.TELEGRAM_BOT_TOKEN:
        print("HATA: TELEGRAM_BOT_TOKEN bulunamadı. Lütfen .env dosyasını kontrol edin.")
        return

    # Telegram Bot uygulamasını oluştur (Ağ gecikmelerine karşı timeout değerleri artırıldı)
    application = (
        ApplicationBuilder()
        .token(config.TELEGRAM_BOT_TOKEN)
        .connect_timeout(60.0)
        .read_timeout(60.0)
        .write_timeout(60.0)
        .build()
    )

    # İşleyicileri (handlers) ekle
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Zamanlanmış görevleri (cron jobs) ayarla (APScheduler telegram.ext içinde JobQueue olarak entegredir)
    job_queue = application.job_queue
    
    # Örnek: Her gün saat 12:00'de su hatırlatıcısı
    # Not: Telegram time beklerken UTC zaman dilimini kullanır, buna göre ayarlama yapılabilir.
    import datetime
    
    # Test aşamasında hızlı sonuç görmek için run_repeating (örneğin her 60 saniyede bir) kullanıyoruz.
    # job_queue.run_repeating(daily_water_reminder, interval=60, first=5)
    
    # Gerçek kullanım için saatlik ayar (Örn: UTC saatiyle 09:00, TR saatiyle 12:00):
    # time_water = datetime.time(hour=9, minute=0, second=0)
    # job_queue.run_daily(daily_water_reminder, time_water)
    
    # time_sport = datetime.time(hour=16, minute=0, second=0) # TR saati 19:00
    # job_queue.run_daily(daily_sport_reminder, time_sport)

    print("Bot başlatılıyor... Çıkış yapmak için Ctrl+C'ye basın.")
    # Botu çalıştır (Polling)
    application.run_polling()

if __name__ == '__main__':
    main()
