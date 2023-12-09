
from typing import Any
import librosa

class Openai_Whisper():
    def __init__(self, language : str, model_name : str = "large-v3") -> None:
        import whisper
        self.whisper_model = whisper.load_model(model_name, download_root = None)
        self.language = language

    def infer(self, audio_in) -> None:
        print("start asr:", audio_in)
        segments = self.whisper_model.transcribe(audio_in, word_timestamps=True, language = self.language)['segments']
        data_list = []
        for _ in segments:
            item = {}
            item['start'] = _['start']
            item['end'] = _['end']
            item['text'] = _['text'].strip()
            data_list.append(item)
        return data_list

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)