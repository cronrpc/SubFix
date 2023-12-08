import os
import shutil
from subfix.models.audio.speaker_diarization import Speech_Campplus_Speaker_Diarization
from subfix.utils import convert_files, get_files_by_ext
from subfix.utils.misc import merge_audio_vads

def diarization_dir(args):


    source_dir = args.source_dir
    target_dir = args.target_dir
    cache_dir = args.cache_dir
    sample_rate = args.sample_rate
    min_seconds = args.min_seconds
    top_of_number = args.top_of_number
    interval = args.interval

    
    dir_16000 = os.path.join(cache_dir,'subfix','origin','16000')
    dir_sample_rate = os.path.join(cache_dir,'subfix','origin',str(sample_rate))

    if os.path.exists(dir_16000):
        shutil.rmtree(dir_16000)
    if os.path.exists(dir_sample_rate):
        shutil.rmtree(dir_sample_rate)
    
    convert_files(source_dir, dir_sample_rate, sample_rate)
    convert_files(dir_sample_rate, dir_16000, 16000)

    files = get_files_by_ext(dir_16000, [".wav"])

    print("Start Speech_Campplus_Speaker_Diarization")

    SCSD = Speech_Campplus_Speaker_Diarization()

    for file_path in files:
        f_16000 = os.path.join(dir_16000, file_path)
        f_samplerate = os.path.join(dir_sample_rate, file_path)
        
        result, topn, topn_number = SCSD.infer(f_16000, min_seconds = min_seconds)
        topn = topn[:top_of_number]
        for person in topn:
            vad_list = []
            save_path = os.path.join(target_dir, os.path.splitext(file_path)[0] + f"_{person}" +  os.path.splitext(file_path)[1])
            print("save:", save_path)
            for item in result:
                if item[2] == person:
                    vad_list.append(item[:2])
            merge_audio_vads(f_samplerate, save_path, vad_list, interval=interval)

    if os.path.exists(dir_16000):
        shutil.rmtree(dir_16000)
    if os.path.exists(dir_sample_rate):
        shutil.rmtree(dir_sample_rate)