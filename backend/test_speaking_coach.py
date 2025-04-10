import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent))

from app.speaking_coach import SpeakingCoach


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


async def test_audio_input(coach):
    """测试音频输入功能"""
    print("\n测试音频输入功能...")
    
    # 这里需要一个音频文件进行测试
    # 如果没有音频文件，可以跳过这个测试
    audio_path = Path("static/test_audio.wav")
    if not audio_path.exists():
        print(f"音频文件不存在: {audio_path}，跳过音频输入测试")
        return
    
    print(f"使用音频文件: {audio_path}")
    
    # 读取音频文件
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    
    # 测试音频输入
    response_text, response_audio = await coach.process_audio_input(audio_bytes)
    print(f"教练回复: {response_text}")
    
    # 保存音频到文件
    response_path = Path("static/test_audio_response.wav")
    with open(response_path, "wb") as f:
        f.write(response_audio)
    print(f"音频已保存到: {response_path}")
    
    # 获取对话历史
    history = await coach.get_conversation_history()
    print(f"对话历史: {history}")


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
    await test_audio_input(coach)
    
    # 测试对话历史
    await test_conversation_history(coach)
    
    print("\n测试完成!")


if __name__ == "__main__":
    asyncio.run(main()) 