from subfix.format import FormatBertvits2
from subfix.models.audio.punctuation import Punctuation_FunASR

def punctuation_multi_lang_process(args):
    input_file = args.load_list
    souce_format = FormatBertvits2()
    data = souce_format.load(input_file)
    punc_fix = Punctuation_FunASR()
    for i in range(len(data)):
        print(i,'/',len(data),sep="")
        data[i]['text'] = punc_fix(data[i]['text'])
    data = souce_format.save(input_file, data)
    pass