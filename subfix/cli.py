import argparse

def handle_webui(args):
    from .webui import startwebui
    startwebui(args)


def handle_create(args):
    print(f"Checkout command with args: {args}")
    if args.solution == "modelscope" and args.language == "ZH":
        from subfix.solution.modelscope_zh import run_task
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
    modelscope_subparsers.add_argument("--resample_dir", type=str, default="origin_resample", help="Resample directory path, Default: origin_resample")
    modelscope_subparsers.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    modelscope_subparsers.add_argument("--language", type=str, default="ZH", help="Language, Default: ZH")
    modelscope_subparsers.add_argument("--output", type=str, default="demo.list", help="List file, Default: demo.list")
    modelscope_subparsers.add_argument("--max_seconds", type=int, default=15, help="Max sliced voice length(seconds), Default: 15")
    modelscope_subparsers.set_defaults(func=handle_create)

    # create whisper
    whisper_subparsers = create_subparsers.add_parser('whisper', 
                                                      help='whisper models')
    whisper_subparsers.add_argument("--source_dir", type=str, default="origin", help="Source directory path, Default: origin")
    whisper_subparsers.add_argument("--target_dir", type=str, default="dataset", help="Target directory path, Default: dataset")
    whisper_subparsers.add_argument("--resample_dir", type=str, default="origin_resample", help="Resample directory path, Default: origin_resample")
    whisper_subparsers.add_argument("--sample_rate", type=int, default=44100, help="Sample rate, Default: 44100")
    whisper_subparsers.add_argument("--language", type=str, default="ZH", help="Language, Default: ZH")
    whisper_subparsers.add_argument("--output", type=str, default="demo.list", help="List file, Default: demo.list")
    whisper_subparsers.add_argument("--max_seconds", type=int, default=15, help="Max sliced voice length(seconds), Default: 15")
    whisper_subparsers.set_defaults(func=handle_create)

    # run
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

