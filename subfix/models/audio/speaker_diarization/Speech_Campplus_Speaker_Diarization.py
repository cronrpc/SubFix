

class Speech_Campplus_Speaker_Diarization():
    def __init__(self) -> None:
        from modelscope.pipelines import pipeline
        self._pipeline = pipeline(
            task='speaker-diarization',
            model='damo/speech_campplus_speaker-diarization_common',
            model_revision='v1.0.0'
        )
    
    def infer(self, input, min_seconds = 0, oracle_num = None, **args):
        result = self._pipeline(input, oracle_num = oracle_num, **args)['text']
        count_dict = {}
        for item in result:
            if item[2] in count_dict:
                count_dict[item[2]] = count_dict[item[2]] + 1
            else:
                count_dict[item[2]] = 1
        numbers = list(reversed([[k, v] for k, v in sorted(count_dict.items(), key=lambda m : list(m)[1])]))
        topn = [i[0] for i in numbers] # person
        topn_number = [i[1] for i in numbers] # number
        res = []
        for item in result:
            if item[1] - item[0] > min_seconds:
                res.append(item)
        return res, topn, topn_number