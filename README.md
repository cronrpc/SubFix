# SubFix
`SubFix` is a web tool designed for easily editing and modifying audio subtitles. Users can see changes in real-time and conveniently **merge, split, delete, and edit subtitles** of audios.

`SubFix` also supports automated voice annotation, utilizing `modelscope` and `whisper` for multilingual text annotation. Currently, `modelscope` provides automated annotations in languages including Chinese, English, Japanese, German, and Russian. `whisper` supports almost all languages."

[中文版本](README_zh.md)

For the old standalone version, please visit [Release V1.2](https://github.com/cronrpc/SubFix/releases/tag/v1.2) to download.

## Installation

Follow these steps for a quick and easy installation. It's recommended to use a `Linux` environment. If using `Windows`, you will need to manually configure the `ffmpeg` environment variable, and installing `modelscope` might be more complex.

### Installing Dependencies

Ensure the installed version of `Python` is above `3.9`, then execute the following command. If you do not need to use automatic labeling of audio, there is no need to install the `Modelscope` module.

Using Conda:
```bash
conda create -n modelscope python=3.9
conda activate modelscope
```

Installing Dependencies:
```bash
sudo apt install build-essential
sudo apt install ffmpeg
sudo apt install libsox-dev

git clone https://github.com/cronrpc/SubFix.git
cd SubFix
pip install "modelscope[audio]" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
pip install -e .
```

## Usage Guide

After installing with `pip install -e .`, you can start the tool from any directory in the `shell` using the following command. All parameters have default values, so you don't need to input any `--option` if the default is used.
```bash
subfix -h

# webui
subfix webui -h
subfix webui --load_list demo.list --webui_language zh --force_delete True
# create dataset
subfix create modelscope -h
# English
subfix create modelscope --source_dir origin --language EN
# Chinese
subfix create modelscope --source_dir origin --language ZH
# Japanese
subfix create modelscope --source_dir origin --language JA
# OpenAI Whisper Annotation (Supports Almost All Languages)
subfix create whisper --source_dir origin --language ZH
subfix create whisper --source_dir origin --language JA
# diarization (speaker segmentation)
subfix diarization -h
subfix diarization --source_dir origin --target_dir diarization --min_seconds 3.0
```

Before using automated annotation, it's recommended to clear the `cache/subfix/` folder.
```bash
rm -rf cache/subfix
```

## Starting SubFix to View Dataset

`SubFix` supports two formats: `.json` and `.list`.

In the `.list` format, each line is similar to `"{wav_path}|{speaker_name}|{language}|{text}"`.

For example, if you already have a `demo.list` file and its corresponding audio files are in the correct path, you can use the following commands to start the `SubFix` UI interface:

```bash
subfix webui --load_list demo.list
# or
subfix webui --load_json demo.json
```

Viewing Help:
```bash
subfix --help
subfix webui --help
```

### Quick Viewing and Listening to Audio

You can click the `Previous Index` and `Next Index` buttons to switch lists, or drag the `slider` and click `Change Index` for quick positioning in the list.

![change index gif](images/index.gif)

### Modifying Text

You can directly modify the text and click the `Submit Text` button to save the changes.

![change text gif](images/text.gif)

### Merging

Select the audios you want to merge, set the `merge interval`, and then click the `merge` button to merge the audio.

![merge audio gif](images/merge.gif)

### Splitting Audio

Select the audio to be split, set the `split point`, and then click the `split` button to proceed. Note that only one audio can be split at a time, and the text needs to be adjusted again after splitting.

![split audio gif](images/split.gif)

### Deleting

Select the audio to be deleted and click the `button` to delete. The delete operation will be temporarily stored in memory. To save it to a file, click the save button or execute another command.

![delete audio gif](images/delete.gif)

### Automated Audio Annotation and Dataset Creation

By default, place the audio files in the `origin` folder. For an audio file `abc.wav` by a speaker `sam`, its file path could be structured like `./origin/sam/abc.wav`. Then execute the following command:

```bash
# rm -rf cache/subfix
subfix create --source_dir origin --output demo.list
```

This command will create a `dataset` directory and store the paths and subtitles of all transcribed audio files in the `demo.list` file.

### Speaker Recognition and Clustering

In some cases, large audio segments might include background music, leading to the recognition of vocals or noise from the background song, causing multiple speakers to be identified in the same file. Or, when speaking is too dense, it might result in excessively long recognized audio.

This feature extracts the `n` most frequent speakers from each file, with an interval of `interval` seconds between each sentence spoken by the same person. This is saved in the `diarization` folder, making it easier to extract audio later.

```bash
subfix diarization --source_dir origin --target_dir diarization --min_seconds 3.0 --interval 10 --top_of_number 1
subfix create modelscope --source_dir diarization --language ZH
```

## Format Conversion

The two formats, `.list` and `.json`, can be converted into each other. Use the following commands to convert files:

```bash
subfix format_convert --source demo.list --target demo.json
subfix format_convert --source demo.json --target demo.list
```

## References

- [anyvoiceai/MassTTS](https://github.com/anyvoiceai/MassTTS)
- [fishaudio/Bert-VITS2](https://github.com/fishaudio/Bert-VITS2)
- [openai/whisper](https://github.com/openai/whisper)