import json
from typing import List


class FormatJson():

    def __init__(self) -> None:
        pass

    def load(self, path : str):
        with open(path, 'r', encoding="utf-8") as source:
            data_lines = source.readlines()
            data = [json.loads(line) for line in data_lines]
            print(f"data has been load from {path}")
        return data

    def save(self, path : str, data : List[dict]):
        with open(path, 'w', encoding="utf-8") as target:
            for item in data:
                line = json.dumps(item, ensure_ascii=False)
                target.write(line + '\n')
            print(f"data has been save at {path}")