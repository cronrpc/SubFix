from typing import Any

class Speech_Fsmn_Vad_Zh_16k_Common():
    def __init__(self) -> None:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        self._inference_pipeline = pipeline(
                                        task=Tasks.voice_activity_detection,
                                        model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
                                        model_revision=None,
                                    )

    def infer(self, audio_in) -> None:
        rec_result = self._inference_pipeline(audio_in = audio_in)
        # return [{start : seconds, end: seconds}]
        data = []
        for item in rec_result['text']:
            data.append(
                {
                    'start' : item[0] / 1000.0,
                    'end'   : item[1] / 1000.0
                }
            )
        return data

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)