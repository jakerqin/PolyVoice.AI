# 模型下载脚本

这个目录包含了用于下载和准备模型的脚本。

## 下载TTS模型

在首次运行应用之前，你需要下载TTS模型到本地。这可以通过以下命令完成：

```bash
cd backend
python scripts/download_models.py
```

这将下载以下模型到 `models/tts` 目录：
- `tts_models/multilingual/multi-dataset/your_tts` - 主要TTS模型
- `tts_models/multilingual/multi-dataset/xtts_v2` - 备用TTS模型

## 模型目录结构

下载后的模型将存储在以下目录结构中：

```
backend/
  models/
    tts/
      tts_models_multilingual_multi-dataset_your_tts/
      tts_models_multilingual_multi-dataset_xtts_v2/
```

## 注意事项

- 模型下载可能需要一些时间，取决于你的网络连接速度
- 下载的模型大约需要1-2GB的磁盘空间
- 一旦模型下载完成，应用将自动使用本地模型，无需再次下载 