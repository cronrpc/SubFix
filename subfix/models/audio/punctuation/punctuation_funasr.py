from typing import Any

class Punctuation_FunASR():
    def __init__(self) -> None:
        from funasr import AutoModel
        self._model = AutoModel(model="ct-punc", model_revision="v2.0.4")
    
    def infer(self, input):
        res = self._model.generate(input=input)
        if (len(res) > 0):
            text = res[0]['text']
            return res
        else:
            return ""
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.infer(*args, **kwds)