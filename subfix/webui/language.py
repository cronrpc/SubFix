
LANG_CONFIG_MAP = {
    "zh": {
        "Change Index" : "改变索引",
        "Submit Text" : "保存文本",
        "Merge Audio" : "合并音频",
        "Delete Audio" : "删除音频",
        "Previous Index" : "前一页",
        "Next Index" : "后一页",
        "Light Theme" : "亮色模式",
        "Dark Theme" : "黑暗模式",
        "Choose Audio" : "选择音频",
        "Output Audio" : "Output Audio",
        "Text" : "文本",
        "Invert Selection": "反选",
        "Save File" : "保存文件",
        "Split Audio" : "分割音频",
        "Audio Split Point(s)" : "音频分割点(单位：秒)",
        "Index":"索引",
        "Interval":"合并间隔（单位：秒）"
    },
}


class TextLanguage():
    def __init__(self, language : str = "en") -> None:
        if language in LANG_CONFIG_MAP.keys():
            self.language = language
        else:
            self.language = "en"
        pass

    def get_text(self, text : str) -> str:
        if self.language == "en":
            return text
        elif text in LANG_CONFIG_MAP[self.language].keys() :
            return LANG_CONFIG_MAP[self.language][text]
        else:
            return text
        
    def __call__(self, text : str) -> str:
        return self.get_text(text)