from typing import Any
import librosa

class Speech_UniASR_Asr_MultiLang():
    def __init__(self, language : str) -> None:
        self.set_asr_model_by_language(language)
        self.set_vad_model_by_language(language)
    
    def set_asr_model_by_language(self, language):

        model_config = {
            "ko" : 'damo/speech_UniASR_asr_2pass-ko-16k-common-vocab6400-tensorflow1-offline',
            "ja" : 'damo/speech_UniASR_asr_2pass-ja-16k-common-vocab93-tensorflow1-offline',
            "en" : 'damo/speech_UniASR_asr_2pass-en-16k-common-vocab1080-tensorflow1-offline',
            "de" : 'damo/speech_UniASR_asr_2pass-de-16k-common-vocab3690-tensorflow1-online',
            "ru" : 'damo/speech_UniASR_asr_2pass-ru-16k-common-vocab1664-tensorflow1-offline',
        }

        model_config_revision = {
            "de" : 'v1.0.1'
        }

        assert( language in model_config.keys() )

        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        revision = model_config_revision[language] if (language in model_config_revision.keys()) else None

        self._asr_model = pipeline( task = Tasks.auto_speech_recognition,
                                    model = model_config[language],
                                    model_revision = revision )

    def set_vad_model_by_language(self, language):
        from subfix.models.audio.vad.speech_fsmn_vad_zh import Speech_Fsmn_Vad_Zh_16k_Common
        self._vad_model = Speech_Fsmn_Vad_Zh_16k_Common()

    def infer(self, audio_in) -> None:
        print("start asr:", audio_in)
        vad_list = self._vad_model(audio_in = audio_in)
        data_list = []
        waveform, sample_rate = librosa.load(audio_in, sr=16000, mono=True)
        for _ in vad_list:
            start_time, end_time = _['start'], _['end']
            start = int(start_time * sample_rate)
            end = int(end_time * sample_rate)
            slice_waveform = waveform[start: end]
            text = self._asr_model(audio_in=slice_waveform)['text']
            print(text)
            if text.strip() == "":
                continue
            item = {}
            item['start'] = start_time
            item['end'] = end_time
            item['text'] = text.strip()
            data_list.append(item)
        return data_list

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)