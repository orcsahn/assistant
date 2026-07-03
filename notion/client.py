import datetime
from notion_client import Client
import config

if config.NOTION_API_KEY:
    notion = Client(auth=config.NOTION_API_KEY)
else:
    notion = None

def get_today_str():
    """Bugünün tarihini YYYY-MM-DD formatında döner."""
    return datetime.date.today().isoformat()

def get_or_create_today_page():
    """Bugüne ait bir sayfa (kayıt) varsa getirir, yoksa oluşturur."""
    if not notion:
        print("Notion istemcisi yapılandırılmamış.")
        return None

    today_str = get_today_str()
    database_id = config.NOTION_DATABASE_ID

    try:
        # Veritabanında bugünün tarihiyle eşleşen bir kayıt var mı diye sorgula
        response = notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "Tarih",
                    "date": {
                        "equals": today_str
                    }
                }
            }
        )
        
        if response["results"]:
            # Kayıt varsa ilkini dön
            return response["results"][0]
        else:
            # Kayıt yoksa yeni oluştur
            new_page = notion.pages.create(
                **{
                    "parent": {"database_id": database_id},
                    "properties": {
                        "İsim": {
                            "title": [
                                {
                                    "text": {
                                        "content": f"Günlük Takip - {today_str}"
                                    }
                                }
                            ]
                        },
                        "Tarih": {
                            "date": {
                                "start": today_str
                            }
                        },
                        "Su": {
                            "checkbox": False
                        },
                        "Spor": {
                            "checkbox": False
                        }
                    }
                }
            )
            return new_page
    except Exception as e:
        print(f"Notion API hatası (get_or_create): {e}")
        return None

def update_habit_status(habit_name: str, status: bool) -> str:
    """Belirli bir alışkanlığın durumunu (checkbox) günceller."""
    if not notion:
        return "Notion API yapılandırılmadığı için işlem gerçekleştirilemedi. Ancak notumu aldım!"

    # 'Su' veya 'Spor' olabilir. Gelen stringi formatlayalım.
    habit_prop_name = habit_name.capitalize()
    
    # Bugünün sayfasını al veya oluştur
    page = get_or_create_today_page()
    if not page:
        return "Notion'da bugüne ait kayıt bulunamadı veya oluşturulamadı."

    page_id = page["id"]

    try:
        # Checkbox'ı güncelle
        notion.pages.update(
            **{
                "page_id": page_id,
                "properties": {
                    habit_prop_name: {
                        "checkbox": status
                    }
                }
            }
        )
        return f"Harika! '{habit_prop_name}' alışkanlığını Notion'da {'tamamlandı' if status else 'tamamlanmadı'} olarak işaretledim."
    except Exception as e:
        print(f"Notion API hatası (update): {e}")
        return f"'{habit_prop_name}' güncellenirken bir hata oluştu. Lütfen veritabanı sütun isimlerini ('Su', 'Spor') kontrol et."
