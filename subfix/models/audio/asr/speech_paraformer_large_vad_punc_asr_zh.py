from typing import Any


class Speech_Paraformer_Large_Vad_Punc_Asr_zh():
    def __init__(self) -> None:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        self._inference_pipeline = pipeline(
            task=Tasks.auto_speech_recognition,
            model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
            model_revision="v1.2.4")

    def infer(self, audio_in) -> None:
        rec_result = self._inference_pipeline(audio_in = audio_in) # dict_keys(['text', 'text_postprocessed', 'time_stamp', 'sentences'])
        data_list = []
        for sentence in rec_result['sentences']:
            if sentence['text'].strip() == "":
                continue
            item = {}
            item['start'] = sentence['ts_list'][0][0] / 1000.0
            item['end'] = sentence['end'] / 1000.0
            item['text'] = sentence['text'].strip()
            data_list.append(item)
        return data_list

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)