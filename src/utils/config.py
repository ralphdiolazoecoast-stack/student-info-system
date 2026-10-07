import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parents[2] / "config" / "config.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
