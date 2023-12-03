import librosa
import os
import soundfile
import subprocess
from concurrent.futures import ThreadPoolExecutor
from .ext_files import get_files_by_ext



def ffmpeg_installed():

    try:
        subprocess.run(["ffmpeg", "-version"], 
                       capture_output=True, 
                       check=True)
        return True
    except Exception as e:
        return False


def convert_wav_ffmpeg(source_file : str, 
                       target_file : str, 
                       sample_rate : int):
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    cmd = ["ffmpeg", "-y", "-i", source_file, "-ar", f"{sample_rate}", "-ac", "1", "-v", "quiet", target_file]

    subprocess.run(cmd, shell=True)


def convert_wav_librosa(source_file : str, 
                        target_file : str, 
                        sample_rate : int):
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    data, sample_rate = librosa.load(source_file, 
                                     sr=sample_rate, 
                                     mono=True)
    
    soundfile.write(target_file, data, sample_rate)


def convert_files(source_dir : str, 
                  target_dir : str, 
                  sample_rate : int, 
                  max_threads = None):

    if max_threads == None:
        max_threads = os.cpu_count()

    ext_files = get_files_by_ext(source_dir, [".mp3","acc","wav"])

    ffmpeg_installed_flag = ffmpeg_installed()

    os.makedirs(target_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for file in ext_files:
            source_path = os.path.join(source_dir, file)
            target_path = os.path.join(target_dir, os.path.splitext(file)[0] + '.wav')
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if not os.path.exists(target_path):
                if ffmpeg_installed_flag:
                    executor.submit(convert_wav_ffmpeg, 
                                    source_path, 
                                    target_path, 
                                    sample_rate)
                else:
                    executor.submit(convert_wav_librosa, 
                                    source_path, 
                                    target_path, 
                                    sample_rate)