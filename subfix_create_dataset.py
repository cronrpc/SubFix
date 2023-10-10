import argparse
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile
from IPython.display import Audio

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


def get_sub_dirs(source_dir):
    sub_dir = [f for f in os.listdir(source_dir) if not f.startswith('.')]
    sub_dir = [f for f in sub_dir if os.path.isdir(os.path.join(source_dir, f))]
    return sub_dir


def is_sentence_ending(sentence):
    if re.search(r'[。？！……]$', sentence):
        return True
    return False


def resample_audios(origin_dir, resample_dir, sample_rate):
    print("start resample audios")
    os.makedirs(resample_dir, exist_ok=True)
    dirs = get_sub_dirs(origin_dir)

    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        ffmpeg_installed = True
        print("ffmpeg installed. use ffmpeg.")
    except Exception as e:
        ffmpeg_installed = False
        print("ERROR! ffmpeg is not installed. use librosa.")

    for dir in dirs:
        source_dir = os.path.join(origin_dir, dir)
        target_dir = os.path.join(resample_dir, dir)
        os.makedirs(target_dir, exist_ok=True)
        listdir = list(os.listdir(source_dir))
        listdir_len = len(listdir)
        for index, f in enumerate(listdir, start=1):
            if f.endswith(".wav") or f.endswith(".mp3"):
                file_path = os.path.join(source_dir, f)
                target_path = os.path.join(target_dir, f)
                target_path = os.path.splitext(target_path)[0] + '.wav'
                if ffmpeg_installed:
                    process = subprocess.run(["ffmpeg", "-y", "-i", file_path, "-ar", f"{sample_rate}", "-ac", "1", "-v", "quiet", target_path])
                else:
                    try:
                        print(f"{index}/{listdir_len} file")
                        data, sample_rate = librosa.load(file_path, sr=sample_rate, mono=True)
                        soundfile.write(target_path, data, sample_rate)
                    except Exception as e:
                        print(f"\n{file_path} convert fail.")
                    finally:
                        pass
                    


def create_dataset(source_dir, target_dir, sample_rate, language, inference_pipeline):
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
            for sentence in rec_result['sentences']:
                text = sentence['text'].strip()
                start = int((sentence['start'] / 1000) * sample_rate)
                end = int((sentence['end'] / 1000) * sample_rate)
                
                if (text == ""):
                    continue
                    
                sentence_list.append(text)
                audio_list.append(data[start:end])
                
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
                    count = count + 1
    return result


def create_list(source_dir, target_dir, resample_dir, sample_rate, language, output_list):

    resample_audios(source_dir, resample_dir, sample_rate)
    
    inference_pipeline = pipeline(
        task=Tasks.auto_speech_recognition,
        model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        model_revision="v1.2.4")

    result =  create_dataset(resample_dir, target_dir, sample_rate = sample_rate, language = language, inference_pipeline = inference_pipeline)

    with open(output_list, "w", encoding="utf-8") as file:
        for line in result:
            try:
                file.write(line.strip() + '\n')
            except UnicodeEncodeError:
                print("UnicodeEncodeError: Can't encode to ASCII:", r)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--source_dir", type=str, default="origin", help="Source directory path")
    parser.add_argument("--target_dir", type=str, default="dataset", help="Target directory path")
    parser.add_argument("--resample_dir", type=str, default="origin_resample", help="Resample directory path")
    parser.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, default is 44100")
    parser.add_argument("--language", type=str, default="ZH", help="Language, default is ZH")
    parser.add_argument("--output", type=str, default="demo.list", help="List file, default is demo.list")

    args = parser.parse_args()

    create_list(args.source_dir, args.target_dir, args.resample_dir, args.sample_rate, args.language, args.output)
    
