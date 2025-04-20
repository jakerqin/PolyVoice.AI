import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent))

from app.speaking_coach import SpeakingCoach


async def test_audio_file_input(audio_file_path: str):
    """
    测试从本地文件读取音频进行对话
    
    Args:
        audio_file_path: 音频文件路径
    """
    print(f"\n测试从文件读取音频功能: {audio_file_path}")
    
    # 检查文件是否存在
    if not Path(audio_file_path).exists():
        print(f"错误: 音频文件不存在 - {audio_file_path}")
        return None
    
    # 创建口语教练实例
    coach = SpeakingCoach()
    
    try:
        # 读取音频文件
        with open(audio_file_path, "rb") as f:
            audio_bytes = f.read()
        
        print(f"已读取音频文件: {audio_file_path} ({len(audio_bytes)} 字节)")
        
        # 处理音频输入
        print("正在处理音频输入...")
        
        # 变量用于保存最终结果
        recognized_text = None
        response_text = None
        response_audio = None
        
        # 使用 async for 处理异步生成器
        async for result in coach.process_audio_input_stream(audio_bytes):
            # 处理不同类型的结果
            if result["type"] == "recognized_text":
                recognized_text = result["data"]
                print(f"识别出的文本: {recognized_text}")
            elif result["type"] == "text":
                # 累积响应文本
                if response_text is None:
                    response_text = result["data"]
                else:
                    response_text += result["data"]
                # 打印进度
                print(f"收到文本块: {result['data']}")
            elif result["type"] == "audio":
                # 保存最后一个音频块
                response_audio = bytes.fromhex(result["data"])
                print(f"收到音频块: {len(response_audio)} 字节")
            elif result["type"] == "error":
                print(f"错误: {result['data']}")
        
        if response_text:
            print(f"完整响应文本: {response_text}")
        
        # 保存响应音频到文件
        if response_audio:
            os.makedirs("static", exist_ok=True)
            response_audio_path = Path("backend/static/audio_response.wav")
            with open(response_audio_path, "wb") as f:
                f.write(response_audio)
            print(f"响应音频已保存到: {response_audio_path}")
        
        # 获取对话历史
        history = await coach.get_conversation_history()
        print(f"对话历史: {history}")
        
        return coach
    
    except Exception as e:
        print(f"处理音频时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """主函数"""
    # 使用脚本所在目录的相对路径
    script_dir = Path(__file__).resolve().parent
    test_file = script_dir / "static" / "test.wav"
    
    if not test_file.exists():
        print(f"错误: 测试文件不存在 - {test_file}")
        return
    
    print(f"测试文件路径: {test_file}")
    coach = await test_audio_file_input(str(test_file))
    
    if coach:
        print("\n测试完成!")


if __name__ == "__main__":
    asyncio.run(main()) 