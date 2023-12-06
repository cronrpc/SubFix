import argparse
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

from subfix.utils import convert_files

def get_sub_dirs(source_dir):
    sub_dir = [f for f in os.listdir(source_dir) if not f.startswith('.')]
    sub_dir = [f for f in sub_dir if os.path.isdir(os.path.join(source_dir, f))]
    return sub_dir


def is_sentence_ending(sentence):
    if re.search(r'[。？！……]$', sentence):
        return True
    return False


def create_dataset(source_dir, target_dir, sample_rate, language, inference_pipeline, max_seconds):
    # source_dir, target_dir, sample_rate=44100, language = "ZH", inference_pipeline = None
    
    roles = get_sub_dirs(source_dir)
    count = 0
    result = []

    for speaker_name in roles:

        source_audios = [f for f in os.listdir(os.path.join(source_dir, speaker_name)) if f.endswith(".wav")]
        source_audios = [os.path.join(source_dir, speaker_name, filename) for filename in source_audios]
        slice_dir = os.path.join(target_dir, speaker_name)
        os.makedirs(slice_dir, exist_ok=True)

        for audio_path in source_audios:
            rec_result = inference_pipeline(audio_in=audio_path) # dict_keys(['text', 'text_postprocessed', 'time_stamp', 'sentences'])
            data, sample_rate = librosa.load(audio_path, sr=sample_rate, mono=True)

            sentence_list = []
            audio_list = []
            time_length = 0
            for sentence in rec_result['sentences']:
                text = sentence['text'].strip()
                if (text == ""):
                    continue
                start = int((sentence['start'] / 1000) * sample_rate)
                end = int((sentence['end'] / 1000) * sample_rate)

                if time_length > 0 and time_length + ((sentence['end'] - sentence['start']) / 1000) > max_seconds:
                    sliced_audio_name = f"{str(count).zfill(6)}"
                    sliced_audio_path = os.path.join(slice_dir, sliced_audio_name+".wav")
                    s_sentence = "".join(sentence_list)
                    if not re.search(r"[。！？]$", s_sentence):
                        sentence_end = s_sentence[-1]
                        s_sentence = s_sentence[:-1] + '。' if sentence_end != '。' else s_sentence
                    audio_concat = np.concatenate(audio_list)
                    if time_length > max_seconds:
                        print(f"[too long voice]:{sliced_audio_path}, voice_length:{time_length} seconds")
                    soundfile.write(sliced_audio_path, audio_concat, sample_rate)
                    result.append(
                        f"{sliced_audio_path}|{speaker_name}|{language}|{s_sentence}"
                    )
                    sentence_list = []
                    audio_list = []
                    time_length = 0
                    count = count + 1

                sentence_list.append(text)
                audio_list.append(data[start:end])
                time_length = time_length + ((sentence['end'] - sentence['start']) / 1000)
                
                if ( is_sentence_ending(text) ):
                    sliced_audio_name = f"{str(count).zfill(6)}"
                    sliced_audio_path = os.path.join(slice_dir, sliced_audio_name+".wav")
                    s_sentence = "".join(sentence_list)
                    audio_concat = np.concatenate(audio_list)
                    soundfile.write(sliced_audio_path, audio_concat, sample_rate)
                    
                    result.append(
                        f"{sliced_audio_path}|{speaker_name}|{language}|{s_sentence}"
                    )
                    sentence_list = []
                    audio_list = []
                    time_length = 0
                    count = count + 1

    return result


def create_list(source_dir, target_dir, resample_dir, sample_rate, language, output_list, max_seconds):

    convert_files(source_dir, resample_dir, sample_rate)
    
    inference_pipeline = pipeline(
        task=Tasks.auto_speech_recognition,
        model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        model_revision="v1.2.4")

    result =  create_dataset(resample_dir, target_dir, sample_rate = sample_rate, language = language, inference_pipeline = inference_pipeline, max_seconds = max_seconds)

    with open(output_list, "w", encoding="utf-8") as file:
        for line in result:
            try:
                file.write(line.strip() + '\n')
            except UnicodeEncodeError:
                print("UnicodeEncodeError: Can't encode to ASCII:", line)


def run_task(args):
    create_list(args.source_dir, args.target_dir, args.resample_dir, args.sample_rate, args.language, args.output, args.max_seconds)
    
