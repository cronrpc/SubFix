import argparse
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile

from subfix.models.audio.asr import Openai_Whisper
from subfix.utils import convert_files
from subfix.utils.misc import merge_audio_slice, get_sub_dirs


def create_whisper_dataset(source_dir, target_dir, sample_rate, language, infer_model, max_seconds, absolute_path : bool):
    # source_dir, target_dir, sample_rate=44100, language = "ZH", inference_pipeline = None
    
    roles = get_sub_dirs(source_dir)
    count = 0
    result = []

    for speaker_name in roles:

        source_audios = [f for f in os.listdir(os.path.join(source_dir, speaker_name)) if f.endswith(".wav")]
        source_audios = [os.path.join(source_dir, speaker_name, filename) for filename in source_audios]
        slice_dir = os.path.join(target_dir, speaker_name)
        os.makedirs(slice_dir, exist_ok=True)

        for audio_path in sorted(source_audios):

            data_list = infer_model(audio_in=audio_path)

            data, count = merge_audio_slice(audio_path, slice_dir, data_list, count, sample_rate, max_seconds, language, speaker_name)

            for item_audio in data:
                if absolute_path:
                    sliced_audio_path = os.path.abspath(item_audio['sliced_audio_path'])
                else:
                    sliced_audio_path = item_audio['sliced_audio_path']
                speaker_name = item_audio['speaker_name']
                language = item_audio['language']
                text = item_audio['text']
                result.append(f"{sliced_audio_path}|{speaker_name}|{language}|{text}")

    return result


def create_whisper_list(source_dir, target_dir, cache_dir, sample_rate, language, output_list, max_seconds, model_name, absolute_path : bool):

    resample_dir = os.path.join(cache_dir,"subfix","origin",f"{sample_rate}")

    convert_files(source_dir, resample_dir, sample_rate)
    
    lang_map = {
        "ZH" : "Chinese",
        "EN" : "English",
        "JA" : "Japanese",
        "RU" : "ru",
        "DE" : "de",
        "KO" : "ko"
    }

    language_map = lang_map[language] if (language in lang_map.keys()) else language 
    
    asr_model = Openai_Whisper(language = language_map, model_name = model_name)

    result =  create_whisper_dataset(resample_dir, target_dir, sample_rate = sample_rate, language = language, infer_model = asr_model, max_seconds = max_seconds, absolute_path = absolute_path)

    with open(output_list, "w", encoding="utf-8") as file:
        for line in result:
            try:
                file.write(line.strip() + '\n')
            except UnicodeEncodeError:
                print("UnicodeEncodeError: Can't encode to ASCII:", line)


def run_whisper_task(args):

    args.absolute_path = (args.absolute_path.upper() == "TRUE")

    create_whisper_list(args.source_dir, args.target_dir, args.cache_dir, args.sample_rate, args.language, args.output, args.max_seconds, args.model, args.absolute_path)
    
