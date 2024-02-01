from typing import Any
import librosa

class Speech_UniASR_Asr_MultiLang():
    def __init__(self, language : str, max_seconds : float) -> None:
        self.set_asr_model_by_language(language)
        self.set_vad_model_by_language(language, max_seconds)
    
    def set_asr_model_by_language(self, language):

        model_config = {
            "KO" : 'damo/speech_UniASR_asr_2pass-ko-16k-common-vocab6400-tensorflow1-offline',
            "JA" : 'damo/speech_UniASR_asr_2pass-ja-16k-common-vocab93-tensorflow1-offline',
            "EN" : 'damo/speech_UniASR_asr_2pass-en-16k-common-vocab1080-tensorflow1-offline',
            "DE" : 'damo/speech_UniASR_asr_2pass-de-16k-common-vocab3690-tensorflow1-online',
            "RU" : 'damo/speech_UniASR_asr_2pass-ru-16k-common-vocab1664-tensorflow1-offline',
            "ZH" : 'iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        }

        model_config_revision = {
            "DE" : 'v1.0.1',
            "ZH" : 'v2.0.4'
        }

        assert( language in model_config.keys() )

        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        revision = model_config_revision[language] if (language in model_config_revision.keys()) else None

        self._asr_model = pipeline( task = Tasks.auto_speech_recognition,
                                    model = model_config[language],
                                    model_revision = revision )

    def set_vad_model_by_language(self, language, max_seconds = 60.0):
        from subfix.models.audio.vad.speech_fsmn_vad_zh import Speech_Fsmn_Vad_Zh_16k_Common
        self._vad_model = Speech_Fsmn_Vad_Zh_16k_Common(max_seconds=max_seconds)

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
            ret_asrmodl = self._asr_model(input = slice_waveform)
            if (len(ret_asrmodl) > 0):
                text = ret_asrmodl[0]['text']
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