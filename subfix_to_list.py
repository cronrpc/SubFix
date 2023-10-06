import os
import json
import click

@click.command()
@click.option('--source_file', prompt='source file', help='source file xxx.json')
@click.option('--target_file', prompt='target file', help='target file xxx.list')
def convert_json_to_list(source_file, target_file):

    with open(source_file, 'r', encoding="utf-8") as source:
        g_data_json = source.readlines()
        g_data_json = [json.loads(line) for line in g_data_json]
    
    with open(target_file, 'w', encoding="utf-8") as target:
        for _ in g_data_json:
            wav_path = _['wav_path']
            speaker_name = _['speaker_name']
            language = _['language']
            text = _['text']
            target.write(f"{wav_path}|{speaker_name}|{language}|{text}\n")
    
    print("Target file has been saved:", target_file)

if __name__ == "__main__":
    print(r"convert json to this format : {wav_path}|{speaker_name}|{language}|{text}")
    convert_json_to_list()