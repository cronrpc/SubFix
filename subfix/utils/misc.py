import re
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


def get_sub_dirs(source_dir):
    sub_dir = [f for f in os.listdir(source_dir) if not f.startswith('.')]
    sub_dir = [f for f in sub_dir if os.path.isdir(os.path.join(source_dir, f))]
    return sub_dir


def ends_with_ending_sentence(sentence):
    if re.search(r'[。？！…]$', sentence):
        return True
    return False


def ends_with_punctuation(sentence):
    pattern = r'[.,!?。，！？、・\uff00-\uffef\u3000-\u303f\u3040-\u309f\u30a0-\u30ff]$'
    return re.search(pattern, sentence)


def merge_audio_slice(source_audio, slice_dir, data_list, start_count, sample_rate, max_seconds, language, speaker_name) -> List:
    # input : datalist = [{'start': seconds, 'end': seconds, 'text': text}]
    # return : [{'sliced_audio_path', 'speaker_name', 'language', 'text'}] , count_next
    sentence_list = []
    audio_list = []
    time_length = 0
    count = start_count
    result = []

    data, sample_rate = librosa.load(source_audio, sr=sample_rate, mono=True)
    for sentence in data_list:
        text = sentence['text'].strip()
        if (text == ""):
            continue
        start = int((sentence['start']) * sample_rate)
        end = int((sentence['end']) * sample_rate)

        if time_length > 0 and time_length + (sentence['end'] - sentence['start']) > max_seconds:
            sliced_audio_name = f"{str(count).zfill(6)}"
            sliced_audio_path = os.path.join(slice_dir, sliced_audio_name+".wav")
            s_sentence = "".join(sentence_list)

            if language == "ZH" and re.search(r"[，]$", s_sentence):
                s_sentence = s_sentence[:-1] + '。'
            if language == "ZH" and not ends_with_punctuation(s_sentence):
                s_sentence = s_sentence + "。"

            audio_concat = np.concatenate(audio_list)
            if time_length > max_seconds:
                print(f"[too long voice]:{sliced_audio_path}, voice_length:{time_length} seconds")
            soundfile.write(sliced_audio_path, audio_concat, sample_rate)
            result.append(
                {
                    'sliced_audio_path' : sliced_audio_path,
                    'speaker_name' : speaker_name,
                    'language' : language,
                    'text' : s_sentence
                }
            )
            sentence_list = []
            audio_list = []
            time_length = 0
            count = count + 1

        sentence_list.append(text)
        audio_list.append(data[start:end])
        time_length = time_length + (sentence['end'] - sentence['start'])
        
        if ( ends_with_ending_sentence(text) ):
            sliced_audio_name = f"{str(count).zfill(6)}"
            sliced_audio_path = os.path.join(slice_dir, sliced_audio_name+".wav")
            s_sentence = "".join(sentence_list)
            audio_concat = np.concatenate(audio_list)
            soundfile.write(sliced_audio_path, audio_concat, sample_rate)
            
            result.append(
                {
                    'sliced_audio_path' : sliced_audio_path,
                    'speaker_name' : speaker_name,
                    'language' : language,
                    'text' : s_sentence
                }
            )
            sentence_list = []
            audio_list = []
            time_length = 0
            count = count + 1
    return result, count