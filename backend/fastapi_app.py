from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import asyncio
from typing import Optional
from pydantic import Field
from app.api import router
from app.speaking_coach import SpeakingCoach

# 创建 FastAPI 应用
app = FastAPI(title="PolyVoice API", description="Backend API for PolyVoice application")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api")

# 创建口语教练实例
speaking_coach = SpeakingCoach()

# 存储任务状态
tasks = {}

@app.get("/")
async def root():
    return {"message": "Welcome to PolyVoice API"} 

@app.post("/task")
async def start_chat(
    background_tasks: BackgroundTasks,
    user_prompt: str = Field(...)
):
    """
    开始聊天接口
    
    Args:
        user_prompt: 用户输入的提示词
        model: 使用的模型（可选，从配置中获取）
        
    Returns:
        任务ID
    """
    # 生成任务ID
    task_id = str(uuid.uuid4())
    
    # 初始化任务状态
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    # 异步处理聊天任务
    background_tasks.add_task(process_chat, task_id, user_prompt)
    
    return {"task_id": task_id}

@app.get("/chat_status/{task_id}")
async def chat_status(task_id: str):
    """
    获取聊天任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        任务状态
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks[task_id]

async def process_chat(task_id: str, user_prompt: str):
    """
    处理聊天任务
    
    Args:
        task_id: 任务ID
        prompt: 用户输入的提示词
        model_name: 使用的模型名称
    """
    try:
        # 更新任务状态为处理中
        tasks[task_id]["status"] = "processing"

        # 调用口语教练处理文本输入
        response_text, response_audio = await speaking_coach.process_text_input(user_prompt)
        
        # 更新任务状态为完成
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = {
            "text": response_text,
            "audio": response_audio.hex() if response_audio else None
        }
    except Exception as e:
        # 更新任务状态为失败
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)




