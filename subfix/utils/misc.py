import os
import json
from typing import List, Union


def save_json(path : str, data : Union[List[dict], dict]):
    with open(path, 'w', encoding="utf-8") as target:
        json.dump(data, path, ensure_ascii=False)
        

def load_json(path : str):
    with open(path, 'r', encoding="utf-8") as source:
        data = json.load(source)
        return data