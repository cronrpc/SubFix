import json
from typing import List


class FormatBertvits2():

    def __init__(self) -> None:
        pass

    def load(self, path : str) -> List[dict]:
        # this format : {wav_path}|{speaker_name}|{language}|{text}"
        data = []
        with open(path, 'r', encoding="utf-8") as source:
            read_list = source.readlines()
            for _ in read_list:
                items = _.split('|')
                if (len(items) == 4):
                    wav_path, speaker_name, language, text= items
                    data.append(
                        {
                            'wav_path':wav_path,
                            'speaker_name':speaker_name,
                            'language':language,
                            'text':text.strip()
                        }
                    )
            print(f"data has been load from {path}")
        return data

    def save(self, path : str, data : List[dict]):
        with open(path, 'w', encoding="utf-8") as target:
            for _ in data:
                wav_path = _['wav_path']
                speaker_name = _['speaker_name']
                language = _['language']
                text = _['text']
                target.write(f"{wav_path}|{speaker_name}|{language}|{text}\n")
            print(f"data has been save at {path}")