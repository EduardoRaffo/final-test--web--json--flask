from types import SimpleNamespace
import json
FILENAME = "users_data.json"
def Load_users():
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content, object_hook=lambda d: SimpleNamespace(**d))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # El archivo existe pero está corrupto o vacío
        return []

def Save_users(users_list):
    # Convierte cada SimpleNamespace a dict
    data = [user.__dict__ for user in users_list]
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
