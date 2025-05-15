# PolyVoice.AI - 智能口语教练

PolyVoice.AI 是一个基于大语言模型和多模态技术的智能口语教练应用，旨在帮助用户提高口语水平。

## 功能特点

- **语音识别**：使用 Whisper 模型将用户的语音转换为文本
- **语音合成**：使用 VALL-E 模型将文本转换为自然流畅的语音
- **智能对话**：使用 DeepSeek-V3 大语言模型进行智能对话和口语评估
- **多语言支持**：支持多种语言的语音识别和合成
- **对话历史**：保存和加载对话历史，方便用户回顾学习过程
- **智能诊断**：分析口语问题并提供针对性教学资源

## 技术栈

- **后端**：FastAPI, Python 3.11
- **大语言模型**：DeepSeek-V3
- **语音识别**：Whisper
- **语音合成**：VALL-E (通过 TTS 库)
- **智能浏览**：Playwright, Browser-Use
- **前端**：React, TypeScript (待实现)

## 安装与使用

### 前提条件

- Python 3.10-3.11
- Poetry (Python 包管理器)
- FFmpeg (用于音频处理)
- Playwright (用于网络内容浏览)

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/yourusername/PolyVoice.AI.git
cd PolyVoice.AI
```

2. 安装依赖

```bash
# 安装 FFmpeg (macOS)
brew install ffmpeg

# 安装 Python 依赖
cd backend
poetry install

# 安装 Playwright 浏览器
# 如果使用 Poetry 环境
poetry run python -m playwright install

# 或者如果在全局环境
python -m playwright install
```

3. 配置

复制 `config/config.example.toml` 到 `config/config.toml`，并填写相应的 API 密钥和配置。

```bash
cp config/config.example.toml config/config.toml
```

4. 运行应用

```bash
poetry run python run.py
```

应用将在 http://localhost:8000 上运行。

## API 接口

### 口语教练 API

- `POST /api/speaking-coach/speak`：处理语音输入，返回文本和音频响应
- `POST /api/speaking-coach/chat`：处理文本输入，返回文本和音频响应
- `GET /api/speaking-coach/history`：获取对话历史
- `POST /api/speaking-coach/history/clear`：清空对话历史
- `POST /api/speaking-coach/history/save`：保存对话历史到文件
- `POST /api/speaking-coach/history/load`：从文件加载对话历史

## 贡献

欢迎提交 Pull Request 或 Issue！

## 许可证

MIT
