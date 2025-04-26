import asyncio
import os
import sys
from pathlib import Path
import base64

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent))

from app.api import speaking_coach


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
    coach = speaking_coach
    
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
        response_audio_chunks = []  # 用于收集所有音频片段
        
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
                # 收集所有音频片段
                audio_chunk = base64.b64decode(result["data"])
                audio_format = result.get("format", "mp3")  # 获取音频格式，默认为mp3
                response_audio_chunks.append(audio_chunk)
                print(f"收到音频块: {len(audio_chunk)} 字节, 格式: {audio_format}")
            elif result["type"] == "error":
                print(f"错误: {result['data']}")
        
        if response_text:
            print(f"完整响应文本: {response_text}")
        
        # 保存合并后的音频到文件
        if response_audio_chunks:
            # 使用脚本所在目录创建正确的路径
            script_dir = Path(__file__).resolve().parent
            audio_dir = script_dir / "static"
            os.makedirs(audio_dir, exist_ok=True)
            
            # 使用绝对路径保存文件
            response_audio_path = audio_dir / "audio_response.mp3"
            
            # 简单合并方式 - 直接写入所有片段
            with open(response_audio_path, "wb") as f:
                for chunk in response_audio_chunks:
                    f.write(chunk)
            print(f"音频片段已合并并保存到: {response_audio_path}，片段数量: {len(response_audio_chunks)}")
        
    
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