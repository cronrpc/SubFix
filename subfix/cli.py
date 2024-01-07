import argparse
import os


def handle_diarization(args):
    print(f"handle_diarization from {args.source_dir} to {args.target_dir}")
    assert(os.path.exists(args.source_dir))
    from subfix.solution.diarization import diarization_dir
    diarization_dir(args)
    pass


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
    args.force_delete = args.force_delete == "True"
    startwebui(args)


def handle_create(args):
    print(f"Checkout command with args: {args}")
    if args.solution == "modelscope":
        from .solution.modelscope_multi_lang import run_task
        run_task(args)
    elif args.solution == "whisper":
        from .solution.whisper_multi_lang import run_whisper_task
        run_whisper_task(args)


def cli():
    parser = argparse.ArgumentParser(description="a tool to check or create TTS dataset")
    subparsers = parser.add_subparsers(dest='command')
    
    # webui
    parser_webui = subparsers.add_parser('webui', 
                                          help='webui to modify audios')
    parser_webui.add_argument('--load_json', default="None", help='source file, like demo.json')
    parser_webui.add_argument('--load_list', default="None", help='source file, like demo.list')
    parser_webui.add_argument('--json_key_text', default="text", type=str, help='the text key name in json, Default: text')
    parser_webui.add_argument('--json_key_path', default="wav_path", type=str, help='the path key name in json, Default: wav_path')
    parser_webui.add_argument('--g_batch', default=10, type=int, help='max number g_batch wav to display, Default: 10')
    parser_webui.add_argument('--webui_language', default="en", type=str, help='webui language: en or zh, Default: en')
    parser_webui.add_argument('--force_delete', default="True", type=str, help='delete file in disk while delete items, True or False, Default: True')
    parser_webui.set_defaults(func=handle_webui)
    

    # create
    parser_create = subparsers.add_parser('create', 
                                          help='create dataset by origin audio dirctory: subfix create [modelscope|whisper]')
    create_subparsers = parser_create.add_subparsers(dest='solution', 
                                                     help='auto asr solution, modelscope or whisper')

    # create modelscope
    modelscope_subparsers = create_subparsers.add_parser('modelscope', 
                                                         help='modelscope models')
    modelscope_subparsers.add_argument("--source_dir", type=str, default="origin", help="Source directory path, Default: origin")
    modelscope_subparsers.add_argument("--target_dir", type=str, default="dataset", help="Target directory path, Default: dataset")
    modelscope_subparsers.add_argument("--cache_dir", type=str, default="cache", help="cache directory path, Default: cache")
    modelscope_subparsers.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    modelscope_subparsers.add_argument("--language", type=str, default="ZH", help="Language, Default: ZH|JA|KO|EN|DE|RU")
    modelscope_subparsers.add_argument("--output", type=str, default="demo.list", help="List file, Default: demo.list")
    modelscope_subparsers.add_argument("--max_seconds", type=int, default=15, help="Max sliced voice length(seconds), Default: 15")
    modelscope_subparsers.set_defaults(func=handle_create)

    # create whisper
    whisper_subparsers = create_subparsers.add_parser('whisper', 
                                                      help='whisper models')
    whisper_subparsers.add_argument("--source_dir", type=str, default="origin", help="Source directory path, Default: origin")
    whisper_subparsers.add_argument("--target_dir", type=str, default="dataset", help="Target directory path, Default: dataset")
    whisper_subparsers.add_argument("--cache_dir", type=str, default="cache", help="cache directory path, Default: cache")
    whisper_subparsers.add_argument("--model", type=str, default="large-v3", help="whisper model small/medium/large-v3, Default: small")
    whisper_subparsers.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    whisper_subparsers.add_argument("--language", type=str, default="ZH", help="Any Language whisper support, Default: ZH")
    whisper_subparsers.add_argument("--output", type=str, default="demo.list", help="List file, Default: demo.list")
    whisper_subparsers.add_argument("--max_seconds", type=int, default=15, help="Max sliced voice length(seconds), Default: 15")
    whisper_subparsers.set_defaults(func=handle_create)

    # format_convert
    parser_format_convert = subparsers.add_parser('format_convert', 
                                          help='format_convert: format_convert --source demo.json --target demo.list')
    parser_format_convert.add_argument('--source', default="demo.list", help='source file, like demo.json/list')
    parser_format_convert.add_argument('--target', default="demo.json", help='target file, like demo.list/json')
    parser_format_convert.set_defaults(func=handle_format_convert)

    # diarization
    parser_diarization = subparsers.add_parser('diarization', 
                                          help='diarization: diarization -h')
    parser_diarization.add_argument('--source_dir', default="origin", help='source dir, Default: origin')
    parser_diarization.add_argument('--target_dir', default="diarization", help='target dir, Default: diarization')
    parser_diarization.add_argument('--cache_dir', default="cache", help='cache dir, Default: cache')
    parser_diarization.add_argument('--min_seconds', default=3.0, type=float, help='slice must bigger than min_seconds, Default: 3.0')
    parser_diarization.add_argument('--top_of_number', default=1, type=int, help='The n items with the highest frequency of occurrence. Default: 1')
    parser_diarization.add_argument('--interval', default=1.0, type=float, help='The interval between two slice audio. Default: 1.0')
    parser_diarization.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    parser_diarization.add_argument("--oracle_num", type=int, default=0, help="oracle number, the person number you think maybe in audio, Default: 0")
    parser_diarization.set_defaults(func=handle_diarization)

    # run
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

