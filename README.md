# SubFix
SubFix is a comprehensive webui-based tool tailored for efficient batch editing, precise subtitle correction, and versatile audio control. Equipped with a user-friendly interface, SubFix ensures that users can easily edit and correct subtitles in bulk while having advanced audio control options.

## Installation

Embark on an effortless setup journey with a straightforward installation process.

### Installing Dependencies

Execute the following commands to install the required dependencies:

```bash
sudo apt install ffmpeg
pip install librosa gradio numpy soundfile
```

### Modelscope Installation (Optional)

To run `subfix_create_dataset.py`, you should be on a Linux system. Ensure that you have conda installed, then create and activate a new environment named "modelscope" with Python 3.8:

```bash
conda create -n modelscope python=3.8
conda activate modelscope
```

Now, install modelscope and upgrade protobuf:

```bash
pip install "modelscope[audio]" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
pip install --upgrade protobuf
pip install librosa gradio numpy soundfile
```

### Crafting the Dataset List

Arrange your data meticulously, following the ./origin/{voice_person}/abc.wav structure, and execute:

```bash
python subfix_create_dataset.py --source_dir origin --output demo.list
```

## Unleashing Web UI Capabilities

Illuminate your editing experience by running SubFix, equipped with either a LIST or JSON file enriched with audio insights:

```bash
python subfix_webui.py --load_list demo.list
# or
python subfix_webui.py --load_json demo.json
```

## Format Conversion

Transition between `.list` and `.json` formats with unprecedented ease, powered by SubFix's intuitive conversion commands:

```bash
python subfix_to_json.py --source_file demo.list --target_file demo.json
python subfix_to_list.py --source_file demo.json --target_file demo.list
```