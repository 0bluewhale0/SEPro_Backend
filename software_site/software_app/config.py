
import json

CONFIG = {}

with open('software_app/config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)