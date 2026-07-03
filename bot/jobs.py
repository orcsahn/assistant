import google.generativeai as genai
import config
import json
import os
from telegram.ext import ContextTypes
from bot.handlers import active_users

# Hatırlatıcı içindeki dinamik mesaj üreticisi için basit bir Gemini kurulumu
def generate_friend_reminder(goal_text: str) -> str:
    if not config.GEMINI_API_KEY:
        return f"🔔 Selam dostum! Günlük hedeflerini ve özellikle şu hedefini unutmadın değil mi: {goal_text} 💪"
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = (
            f"Kullanıcının kaydettiği uzun vadeli hedefleri şunlar: '{goal_text}'. "
            "Ayrıca her gün 'Su' ve 'Spor' takibi de yapıyor. "
            "Kullanıcıya akşam hatırlatması yapan samimi, çok yakın, esprili ve motive edici bir arkadaş gibi kısa bir mesaj yaz. "
            "Resmi olma, emoji kullan. Doğrudan mesaja başla."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Dinamik hatırlatıcı üretilirken hata: {e}")
        return f"🔔 Selam! Su, spor ve şu hedefini unutmadın umarım: {goal_text} 😉"

async def daily_water_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Kullanıcılara her gün hedeflerini akıllıca hatırlatan proaktif fonksiyon."""
    
    # Bellekte kayıtlı tüm aktif kullanıcılara mesaj gönder
    for chat_id in list(active_users):
        goal_text = "Henüz özel bir hedef belirtilmedi."
        
        # utils/storage.py'nin kaydettiği JSON dosyasını okumaya çalışalım
        # Dosya adı muhtemelen habit-tracker içindeki yapılara göre şekillenmiştir
        # Eğer utils/storage kodun farklıysa buradaki dosya yolunu güncelleyebiliriz
        json_path = "user_goals.json" 
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    goals_data = json.load(f)
                    # Chat ID'ye ait hedefi çekelim
                    if str(chat_id) in goals_data:
                        goal_text = goals_data[str(chat_id)]
            except Exception as e:
                print(f"Hedef dosyası okunurken hata oluştu: {e}")

        # Gemini ile arkadaşça dinamik mesajı üretelim
        dynamic_message = generate_friend_reminder(goal_text)
        
        try:
            await context.bot.send_message(chat_id=chat_id, text=dynamic_message)
        except Exception as e:
            print(f"Kullanıcıya ({chat_id}) mesaj gönderilemedi: {e}")

async def daily_sport_reminder(context: ContextTypes.DEFAULT_TYPE):
    # İki hatırlatıcıyı tek bir akıllı hatırlatıcıda birleştirdiğimiz için 
    # main.py'deki repeating job zaten daily_water_reminder'ı tetikleyecek.
    pass