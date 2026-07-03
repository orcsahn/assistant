from telegram import Update
from telegram.ext import ContextTypes
from ai.gemini import GeminiChat

user_chats = {}
active_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_users.add(chat_id)
    
    if chat_id not in user_chats:
        user_chats[chat_id] = GeminiChat(chat_id=chat_id)
        
    welcome_message = (
        "Selam Orçun dostum! Ben senin kişisel yaşam koçun ve en yakın yol arkadaşınım. 😎\n\n"
        "Bana günlük alışkanlıklarını söyleyebilir (Su, Spor) veya hayata dair yepyeni uzun vadeli hedeflerinden (İngilizce öğrenmek, kitap okumak vb.) bahsedebilirsin.\n\n"
        "Hepsini aklıma yazacağım ve seni her gün proaktif olarak darlayacağım! Hazırsan başlayalım. 🔥"
    )
    await context.bot.send_message(chat_id=chat_id, text=welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_users.add(chat_id)
    text = update.message.text
    
    if chat_id not in user_chats:
        user_chats[chat_id] = GeminiChat(chat_id=chat_id)
        
    bot_chat = user_chats[chat_id]
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    
    response_text = bot_chat.send_message(text)
    await context.bot.send_message(chat_id=chat_id, text=response_text)