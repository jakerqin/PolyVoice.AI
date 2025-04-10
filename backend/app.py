from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import router as speaking_coach_router

app = FastAPI(title="PolyVoice API", description="Backend API for PolyVoice application")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 添加API路由
app.include_router(speaking_coach_router, prefix="/api/speaking-coach", tags=["speaking-coach"])

@app.get("/")
async def root():
    return {"message": "Welcome to PolyVoice API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)