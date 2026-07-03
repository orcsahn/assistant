from notion.client import update_habit_status
from utils.storage import save_user_goal

def get_habit_tools(chat_id: int):
    def mark_habit_done(habit_name: str) -> str:
        """Kullanıcı 'Su' içtiğini veya 'Spor' yaptığını belirttiğinde bu fonksiyon çağrılır. habit_name sadece 'Su' veya 'Spor' olabilir."""
        return update_habit_status(habit_name, True)

    def mark_habit_undone(habit_name: str) -> str:
        """Kullanıcı su içmediğini veya spor yapmadığını belirttiğinde bu fonksiyon çağrılır."""
        return update_habit_status(habit_name, False)

    def set_user_goal(goal_description: str) -> str:
        """Kullanıcı İngilizce öğrenmek, kitap okumak, kilo vermek, yazılım çalışmak gibi uzun vadeli YENİ veya BAŞKA bir hedef/alışkanlık söylediğinde bu fonksiyon çağrılır."""
        save_user_goal(chat_id, goal_description)
        return f"'{goal_description}' hedefi hafızaya başarıyla kaydedildi. Kullanıcıya bir dost gibi, bu yeni hedefi ajandana yazdığını ve her gün ona bunu hatırlatacağını çok samimi bir dille söyle."

    return [mark_habit_done, mark_habit_undone, set_user_goal]