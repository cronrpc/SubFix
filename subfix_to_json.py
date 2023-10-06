import os
import json
import click

@click.command()
@click.option('--source_file', prompt='source file', help='source file xxx.list')
@click.option('--target_file', prompt='target file', help='target file xxx.json')
def convert_list_to_json(source_file, target_file):

    with open(source_file, 'r', encoding="utf-8") as source:
        g_data_list = source.readlines()
    
    with open(target_file, 'w', encoding="utf-8") as target:
        output = []
        for _ in g_data_list:
            data = _.split('|')
            if (len(data) == 4):
                wav_path, speaker_name, language, text= data
                output.append(
                    json.dumps(
                        {
                            'wav_path':wav_path,
                            'speaker_name':speaker_name,
                            'language':language,
                            'text':text.strip()
                        },
                        ensure_ascii = False
                    ) +'\n'
                )
            else:
                print("error line:", data)

        for line in output:
            target.write(line)
    
    print("Target file has been saved:", target_file)

if __name__ == "__main__":
    print(r"convert list to json format : {wav_path:'hello.wav', text:'hello', ...}")
    convert_list_to_json()