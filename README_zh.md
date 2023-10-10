# SubFix
`SubFix`是一个用于轻松地编辑修改音频字幕的网页工具。能够实时地看到改动，方便地对音频进行**合并、分割、删除、编辑字幕**，同时能够马上知道改动后的效果。

[English Version](README.md)

## 安装

进行如下安装步骤可以快速而轻松的安装。建议使用`Linux`环境，如果是`Windows`环境，需要您手动配置`ffmpeg`环境变量。

### 安装依赖

确认安装的`Python`版本大于`3.8`，然后执行如下命令。如果您不需要使用音频的自动标注，那么不需要安装`Modelscope`模块。

```bash
pip install librosa gradio numpy soundfile
```

## 启动SubFix查看数据集

`SubFix`支持2种格式，分别是`.json`和`.list`格式。

`.list`的格式中，每行数据类似于`"{wav_path}|{speaker_name}|{language}|{text}"`。

例如，如果你已经有了一个`demo.list`文件，和它对应的音频已经放到了正确的路径，那么可以执行如下命令来启动`SubFix`的UI界面：

```bash
python subfix_webui.py --load_list demo.list
# or
python subfix_webui.py --load_json demo.json
```

### 快速查看和听取音频

可以点击`Previous Index`、`Next Index`按钮来切换列表，同时可以拖动`slider`并点击`Change Index`来快速定位列表。

![change index gif](images/index.gif)

### 修改文本

可以直接修改文本，并点击`Submit Text`按钮来保存修改。

![change text gif](images/text.gif)

### 合并

选择需要合并的音频，设置`合并间隔`，然后点击`合并`按钮来合并音频。

![merge audio gif](images/merge.gif)

### 分割音频

选择需要分割的音频，设置`分割点`，然后点击`分割`按钮来进行分割。注意，一次只能分割一个音频，分割后需要重新调整下文本。

![split audio gif](images/split.gif)

### 删除

选择需要删除的音频，点击`按钮`进行删除。删除操作将暂存到内存之中，如果需要保存到文件中，需要点击保存按钮，或者执行一次其他命令来保存。

![delete audio gif](images/delete.gif)

## Modelscope 安装 (可选)

如果需要执行 `subfix_create_dataset.py` 来进行原始音频的自动标注, 您需要在`Linux`下执行如下命令，并且最好使得`Python`版本是`3.8/3.9`版本。这里提供一个使用`conda`的方式来保证`Python`环境是`3.8`版本。

```bash
conda create -n modelscope python=3.8
conda activate modelscope
```

然后，安装`ffmpeg`，安装`modelscope`模块，并且升级`protobuf`模块:

```bash
sudo apt install ffmpeg

pip install "modelscope[audio]" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
pip install --upgrade protobuf
pip install librosa gradio numpy soundfile
```

### 自动标注音频和创建数据集

默认情况下，将音频文件放入`origin`文件夹下，对于一个`sam`音频文件`abc.wav`，其所在的文件路径可以是`./origin/sam/abc.wav`这样的结构，之后执行下面的命令：

```bash
python subfix_create_dataset.py --source_dir origin --output demo.list
```

该命令将创建一个`dataset`目录，同时将所有文件转录的音频的路径和字幕存储到了`demo.list`文件中。



## 格式转换

两种格式`.list`和`.json`可以互相转换，使用如下命令对文件进行转换：

```bash
python subfix_to_json.py --source_file demo.list --target_file demo.json
python subfix_to_list.py --source_file demo.json --target_file demo.list
```