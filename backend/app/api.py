import uuid
from fastapi import APIRouter, Body, BackgroundTasks, HTTPException
from app.speaking_coach import SpeakingCoach
from app.logger import logger

router = APIRouter()
# 存储任务状态
tasks = {}

# 创建口语教练实例
speaking_coach = SpeakingCoach()

@router.post("/task")
async def start_chat(
    background_tasks: BackgroundTasks,
    user_prompt: str = Body(...)
):
    """
    开始聊天接口
    
    Args:
        request: 包含用户提示词的请求体
        
    Returns:
        任务ID
    """
    # 生成任务ID
    task_id = str(uuid.uuid4())
    logger.info(f"开始聊天任务: {task_id}, 用户提示词: {user_prompt}")
    # 初始化任务状态
    tasks[task_id] = {
        "status": "pending",
        "result": None,
        "error": None
    }
    
    # 异步处理聊天任务
    background_tasks.add_task(process_chat, task_id, user_prompt)
    
    return {"task_id": task_id}

@router.get("/chat_status/{task_id}")
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
        logger.info(f"处理聊天任务: {task_id}, 用户提示词: {user_prompt}")
        
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
        logger.error(f"处理聊天任务失败: {task_id}, 错误信息: {str(e)}")
