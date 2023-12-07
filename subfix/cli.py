import argparse
import os


def handle_format_convert(args):
    from .format import FormatBertvits2, FormatJson
    print(os.path.splitext(args.source)[1])
    if os.path.splitext(args.source)[1] == '.list':
        souce_format = FormatBertvits2()
    else:
        souce_format = FormatJson()

    if os.path.splitext(args.target)[1] == '.list':
        target_format = FormatBertvits2()
    else:
        target_format = FormatJson()

    data = souce_format.load(args.source)
    target_format.save(args.target, data)
        


def handle_webui(args):
    from .webui import startwebui
    startwebui(args)


def handle_create(args):
    print(f"Checkout command with args: {args}")
    if args.solution == "modelscope" and args.language == "ZH" and args.revision == "1.0":
        from .solution.modelscope_zh_v1 import run_task
        run_task(args)


def cli():
    parser = argparse.ArgumentParser(description="a tool to check or create TTS dataset")
    subparsers = parser.add_subparsers(dest='command')
    
    # webui
    parser_webui = subparsers.add_parser('webui', 
                                          help='webui to modify audios')
    parser_webui.add_argument('--load_json', default="None", help='source file, like demo.json')
    parser_webui.add_argument('--load_list', default="None", help='source file, like demo.list')
    parser_webui.add_argument('--json_key_text', default="text", help='the text key name in json, Default: text')
    parser_webui.add_argument('--json_key_path', default="wav_path", help='the path key name in json, Default: wav_path')
    parser_webui.add_argument('--g_batch', default=10, help='max number g_batch wav to display, Default: 10')
    parser_webui.add_argument('--webui_language', default="en", help='webui language: en or zh, Default: en')
    parser_webui.set_defaults(func=handle_webui)
    

    # create
    parser_create = subparsers.add_parser('create', 
                                          help='create dataset by origin audio dirctory')
    create_subparsers = parser_create.add_subparsers(dest='solution', 
                                                     help='auto asr solution, modelscope or whisper')

    # create modelscope
    modelscope_subparsers = create_subparsers.add_parser('modelscope', 
                                                         help='modelscope models')
    modelscope_subparsers.add_argument("--source_dir", type=str, default="origin", help="Source directory path, Default: origin")
    modelscope_subparsers.add_argument("--target_dir", type=str, default="dataset", help="Target directory path, Default: dataset")
    modelscope_subparsers.add_argument("--cache_dir", type=str, default="cache", help="cache directory path, Default: cache")
    modelscope_subparsers.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    modelscope_subparsers.add_argument("--language", type=str, default="ZH", help="Language, Default: ZH")
    modelscope_subparsers.add_argument("--output", type=str, default="demo.list", help="List file, Default: demo.list")
    modelscope_subparsers.add_argument("--max_seconds", type=int, default=15, help="Max sliced voice length(seconds), Default: 15")
    modelscope_subparsers.add_argument("--revision", type=str, default="1.0", help="the modelscope sulotions: 1.0 or 2.0; default: 1.0")
    modelscope_subparsers.set_defaults(func=handle_create)

    # create whisper
    whisper_subparsers = create_subparsers.add_parser('whisper', 
                                                      help='whisper models')
    whisper_subparsers.add_argument("--source_dir", type=str, default="origin", help="Source directory path, Default: origin")
    whisper_subparsers.add_argument("--target_dir", type=str, default="dataset", help="Target directory path, Default: dataset")
    whisper_subparsers.add_argument("--cache_dir", type=str, default="cache", help="cache directory path, Default: cache")
    whisper_subparsers.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    whisper_subparsers.add_argument("--language", type=str, default="ZH", help="Language, Default: ZH")
    whisper_subparsers.add_argument("--output", type=str, default="demo.list", help="List file, Default: demo.list")
    whisper_subparsers.add_argument("--max_seconds", type=int, default=15, help="Max sliced voice length(seconds), Default: 15")
    whisper_subparsers.set_defaults(func=handle_create)

    # format_convert
    parser_format_convert = subparsers.add_parser('format_convert', 
                                          help='format_convert: format_convert --source demo.json --target demo.list')
    parser_format_convert.add_argument('--source', default="demo.list", help='source file, like demo.json/list')
    parser_format_convert.add_argument('--target', default="demo.json", help='target file, like demo.list/json')
    parser_format_convert.set_defaults(func=handle_format_convert)

    # run
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

