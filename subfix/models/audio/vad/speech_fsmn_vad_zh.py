from typing import Any

class Speech_Fsmn_Vad_Zh_16k_Common():
    def __init__(self, max_seconds : float = 60.0) -> None:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        self._inference_pipeline = pipeline(
                                        task=Tasks.voice_activity_detection,
                                        model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
                                        model_revision=None,
                                    )
        self.max_seconds = max_seconds
        self._tolerance = 1e-6

    def infer(self, audio_in) -> None:
        rec_result = self._inference_pipeline(audio_in)[0]
        # return [{start : seconds, end: seconds}]
        data = []
        for item in rec_result['value']:
            start = item[0] / 1000.0
            end = item[1] / 1000.0
            duration = end - start
            if duration <= self.max_seconds:
                data.append({'start': start, 'end': end})
            else:
                num_segments = int(duration / self.max_seconds) + (1 if duration % self.max_seconds > self._tolerance else 0)
                segment_length = duration / num_segments
                for i in range(num_segments):
                    new_start = start + i * segment_length
                    new_end = min(new_start + segment_length, end)
                    data.append({'start': new_start, 'end': new_end})
        return data

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)