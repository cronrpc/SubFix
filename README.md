# SubFix
A web-based tool designed for efficient batch editing, accurate subtitle correction, and versatile audio control.

## INSTALLATION

Execute the following commands to install the required dependencies:

```bash
sudo apt install ffmpeg
pip install librosa gradio numpy soundfile
```

## USAGE

Run SubFix with a JSON file containing audio information as follows:

```bash
python subfix_webui.py --source_json audios_information.json
```

## FORMAT CONVERSION

Easily convert your .list files to .json, edit your audios using the SubFix web interface, and then convert them back to .list format with the commands below:

```bash
python subfix_to_json.py --source_file demo.list --target_file demo.json
python subfix_webui.py --source_json demo.json
python subfix_to_list.py --source_file demo.json --target_file demo_remake.list
```