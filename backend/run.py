import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).resolve().parent))

import uvicorn
from fastapi_app import app


def main():
    """启动应用程序"""
    # 确保静态目录存在
    os.makedirs("static", exist_ok=True)
    
    # 启动应用程序
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    main() 