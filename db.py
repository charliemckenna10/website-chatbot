import json
from pathlib import Path

FILE = Path("usage.json")

def _load():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return {}

def get_tokens_used(user_id):
    data = _load()
    return data.get(user_id, 0)

def save_tokens_used(user_id, tokens):
    data = _load()
    data[user_id] = data.get(user_id, 0) + tokens
    FILE.write_text(json.dumps(data))
