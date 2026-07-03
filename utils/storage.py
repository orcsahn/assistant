import json
import os

STORAGE_FILE = "users_goals.json"

def _load_data():
    if not os.path.exists(STORAGE_FILE):
        return {}
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_data(data):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_user_goal(chat_id: int, goal: str):
    data = _load_data()
    data[str(chat_id)] = goal
    _save_data(data)

def get_user_goal(chat_id: int) -> str:
    data = _load_data()
    return data.get(str(chat_id), None)
