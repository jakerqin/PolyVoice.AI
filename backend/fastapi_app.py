from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

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





@app.get("/")
async def root():
    return {"message": "Welcome to PolyVoice API"} 




