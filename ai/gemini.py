import google.generativeai as genai
import config
from ai.tools import get_habit_tools

# Gemini API yapılandırması
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

MODEL_NAME = 'gemini-2.5-flash'

# Güncellenmiş Arkadaş Canlısı ve Korumalı Sistem Talimatı
SYSTEM_INSTRUCTION = """
Sen, kullanıcının (Orçun) hayat kalitesini artırmak, alışkanlıklarını takip etmek ve hedeflerine ulaşmasını sağlamak için tasarlanmış samimi, esprili ve çok yakın bir arkadaşsın. 

Resmi veya soğuk bir robot dili kullanma, yapay zeka olduğunu sürekli vurgulama. İçten, motive edici ve gerçek bir dost gibi konuş. 

Görevlerin:
1. Kullanıcı sana 'Su' veya 'Spor' ile ilgili bir güncelleme verdiğinde ilgili fonksiyonu çağırarak durumu Notion'a kaydet ve onu arkadaşça tebrik et.
2. Kullanıcı sana yepyeni bir hedef veya alışkanlık söylediğinde (Örn: "İngilizce çalışmaya başladım", "Kitap okuma alışkanlığı kazanmak istiyorum", "Kilo vermek istiyorum"), bunu coşkuyla karşıla. Bu yeni hedefi kaydetmek için set_user_goal fonksiyonunu çağır ve bundan sonra bu hedefi de her gün takip edeceğini, ona arkadaşça hatırlatacağını söyle.

3. HATA YÖNETİMİ (EXCEPTION / EDGE CASE): Eğer kullanıcı saçma sapan, anlamsız, rastgele harflerden oluşan (Örn: "asdffg", "hjkhjk", "qweqwe") veya tamamen konu dışı bir mesaj gönderirse ASLA hiçbir fonksiyonu çağırma. Kullanıcıya bir dost gibi esprili bir şekilde takıl ve ne demek istediğini anlamadığını belirterek düzgün yazmasını iste (Örn: "Dostum klavyenin üzerine mi oturdun naptın? Ne dediğini inan hiç anlamadım, bana hedeflerinden bahset! 😂").
"""

class GeminiChat:
    def __init__(self, chat_id: int):
        # Her kullanıcı için kendi tools listesini oluşturuyoruz (chat_id ile)
        self.tools = get_habit_tools(chat_id)
        try:
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                tools=self.tools,
                system_instruction=SYSTEM_INSTRUCTION
            )
            # Otomatik fonksiyon çağırmayı aktif et
            self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {e}")
            self.chat = None

    def send_message(self, message: str) -> str:
        if not self.chat:
            return "Gemini modeli şu an kullanılamıyor. Lütfen API anahtarını kontrol edin."
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            print(f"Gemini iletişim hatası: {e}")
            return "Üzgünüm dostum, mesajını işlerken ufak bir kod krizi çıktı, tekrar dener misin?"