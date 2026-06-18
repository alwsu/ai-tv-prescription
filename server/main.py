"""
@ai-generated true 2026-06-18
文件名: main.py
作用: FastAPI 应用入口 — CORS、路由注册、启动钩子
启动: python main.py 或 uvicorn main:app --reload --port 8000
文档: http://localhost:8000/docs
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_database
from routes import recommend, history, preferences, stats


# @ai-generated true 2026-06-18
app = FastAPI(
    title="AI 追剧处方 API",
    description="基于心情和碎片时间的影视推荐后端",
    version="1.0.0",
)

# @ai-generated true 2026-06-18
# 跨域配置 — Demo 阶段允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @ai-generated true 2026-06-18
@app.on_event("startup")
def on_startup() -> None:
    """应用启动时初始化数据库与种子数据"""
    init_database()
    print("[Rx Drama] 数据库初始化完成")


# @ai-generated true 2026-06-18
@app.get("/", tags=["root"])
def root() -> dict:
    """健康检查接口"""
    return {
        "name": "AI 追剧处方 API",
        "version": "1.0.0",
        "docs": "/docs",
    }


# 注册业务路由
app.include_router(recommend.router)
app.include_router(history.router)
app.include_router(preferences.router)
app.include_router(stats.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
