from typing import Any


class Speech_Paraformer_Large_Vad_Punc_Asr_zh():
    def __init__(self, language : str = "ZH") -> None:
        from funasr import AutoModel

        self._model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                  vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                  punc_model="ct-punc-c", punc_model_revision="v2.0.4",
                  spk_model="cam++", spk_model_revision="v2.0.2",
                  )

    def infer(self, audio_in) -> None:
        rec_result = self._model.generate(input=audio_in, 
                                    batch_size_s=300, 
                                    hotword='') # dict_keys(['text', 'start', 'end', 'timestamp', 'spk'])
        data_list = []
        for sentence in rec_result[0]['sentence_info']:
            if sentence['text'].strip() == "":
                continue
            item = {}
            item['start'] = sentence['timestamp'][0][0] / 1000.0
            item['end'] = sentence['end'] / 1000.0
            item['text'] = sentence['text'].strip()
            data_list.append(item)
        return data_list

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)