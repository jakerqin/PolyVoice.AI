import asyncio
import os
import sys
import wave
import pyaudio
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent))

from app.speaking_coach import SpeakingCoach


def list_audio_devices():
    """
    列出所有可用的音频设备
    
    Returns:
        输入设备列表
    """
    audio = pyaudio.PyAudio()
    input_devices = []
    
    print("\n可用的音频输入设备:")
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # 只显示输入设备
            print(f"设备 {i}: {device_info['name']}")
            input_devices.append(i)
    
    audio.terminate()
    return input_devices


def record_audio(duration=5, sample_rate=16000, channels=1, chunk=1024, device_index=None):
    """
    录制音频
    
    参数:
        duration: 录音时长(秒)
        sample_rate: 采样率
        channels: 声道数
        chunk: 每次读取的帧数
        device_index: 设备索引，如果为None则使用默认设备
    
    返回:
        录制的音频数据
    """
    print(f"准备录音，请说话... ({duration}秒)")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("开始录音!")
    
    audio = pyaudio.PyAudio()
    
    # 如果没有指定设备，尝试使用默认设备
    if device_index is None:
        try:
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk
            )
        except OSError:
            # 如果默认设备不可用，列出所有设备并让用户选择
            input_devices = list_audio_devices()
            if not input_devices:
                raise OSError("没有找到可用的音频输入设备")
            
            # 使用第一个可用的输入设备
            device_index = input_devices[0]
            print(f"使用设备 {device_index} 进行录音")
            
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=chunk
            )
    else:
        # 使用指定的设备
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=chunk
        )
    
    frames = []
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("录音结束!")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    return frames


def save_audio_to_wav(frames, filename, sample_rate=16000, channels=1):
    """
    将录制的音频保存为WAV文件
    
    参数:
        frames: 录制的音频帧
        filename: 保存的文件名
        sample_rate: 采样率
        channels: 声道数
    """
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"音频已保存到: {filename}")


async def test_text_input():
    """测试文本输入功能"""
    print("测试文本输入功能...")
    
    # 创建口语教练实例
    coach = SpeakingCoach()
    
    # 测试文本输入
    text = "你好，我想提高我的英语口语水平。"
    print(f"用户输入: {text}")
    
    response_text, response_audio = await coach.process_text_input(text)
    print(f"教练回复: {response_text}")
    
    # 保存音频到文件
    audio_path = Path("static/test_response.wav")
    with open(audio_path, "wb") as f:
        f.write(response_audio)
    print(f"音频已保存到: {audio_path}")
    
    # 获取对话历史
    history = await coach.get_conversation_history()
    print(f"对话历史: {history}")
    
    return coach


async def test_audio_input():
    """测试音频输入功能"""
    print("\n测试音频输入功能...")
    
    # 创建口语教练实例
    coach = SpeakingCoach()
    
    # 列出可用的音频设备
    input_devices = list_audio_devices()
    if not input_devices:
        print("错误: 没有找到可用的音频输入设备!")
        return None
    
    # 录制音频
    print("请准备一段简短的语音输入...")
    audio_frames = record_audio(duration=5, device_index=input_devices[0])  # 录制5秒
    
    # 保存录制的音频
    test_audio_path = Path("static/test_audio.wav")
    save_audio_to_wav(audio_frames, str(test_audio_path))
    
    # 读取录制的音频文件
    with open(test_audio_path, "rb") as f:
        audio_bytes = f.read()
    
    print(f"已读取录制的音频文件: {test_audio_path}")
    
    # 处理音频输入
    print("正在处理音频输入...")
    response_text, response_audio = await coach.process_audio_input(audio_bytes)
    print(f"识别出的文本: {response_text}")
    print(f"教练回复: {response_text}")
    
    # 保存响应音频到文件
    response_audio_path = Path("static/audio_response.wav")
    with open(response_audio_path, "wb") as f:
        f.write(response_audio)
    print(f"响应音频已保存到: {response_audio_path}")
    
    # 获取对话历史
    history = await coach.get_conversation_history()
    print(f"对话历史: {history}")
    
    return coach


async def test_conversation_history(coach):
    """测试对话历史功能"""
    print("\n测试对话历史功能...")
    
    # 保存对话历史
    history_path = Path("static/conversation_history.json")
    await coach.save_conversation_history(str(history_path))
    print(f"对话历史已保存到: {history_path}")
    
    # 清空对话历史
    await coach.clear_conversation_history()
    print("对话历史已清空")
    
    # 加载对话历史
    await coach.load_conversation_history(str(history_path))
    print("对话历史已加载")
    
    # 获取对话历史
    history = await coach.get_conversation_history()
    print(f"对话历史: {history}")


async def main():
    """主函数"""
    # 确保静态目录存在
    os.makedirs("static", exist_ok=True)
    
    # 测试文本输入
    coach = await test_text_input()
    
    # 测试音频输入
    audio_coach = await test_audio_input()
    if audio_coach:
        coach = audio_coach
    
    # 测试对话历史
    await test_conversation_history(coach)
    
    print("\n测试完成!")


if __name__ == "__main__":
    asyncio.run(main()) 