import os
import json
from typing import List, Union
import librosa
import soundfile
import numpy as np

def save_json(path : str, data : Union[List[dict], dict]):
    with open(path, 'w', encoding="utf-8") as target:
        json.dump(data, path, ensure_ascii=False)


def load_json(path : str):
    with open(path, 'r', encoding="utf-8") as source:
        data = json.load(source)
        return data


def merge_audio_vads(source_path ,save_path, vad_list : List[List], interval = 1, sample_rate = None):
    data, sample_rate = librosa.load(source_path, sr=sample_rate, mono=True)
    audio_list = []
    for i, _ in enumerate(vad_list):
        time_start = _[0]
        time_end = _[1]
        start = int((time_start) * sample_rate)
        end = int((time_end) * sample_rate)
        if (i > 0):
            silence = np.zeros(int(sample_rate * interval))
            audio_list.append(silence)
        audio_list.append(data[start:end])
    audio_concat = np.concatenate(audio_list)
    os.makedirs(os.path.split(save_path)[0], exist_ok=True)
    soundfile.write(save_path, audio_concat, sample_rate)