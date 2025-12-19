"""
Tremor Guard Backend - Main Application
震颤卫士后端 - 主应用入口

FastAPI 应用配置和路由注册
支持单容器部署（前后端合一）
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import auth, device, data, analysis, ai, report, test, config

# 静态文件目录（前端构建产物）
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print(f"🚀 {settings.APP_NAME} 启动中...")
    print(f"📊 环境: {settings.APP_ENV}")

    # TODO: 初始化数据库连接
    # TODO: 初始化 Redis 连接

    yield

    # 关闭时执行
    print(f"👋 {settings.APP_NAME} 关闭中...")
    # TODO: 关闭数据库连接
    # TODO: 关闭 Redis 连接


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    description="帕金森震颤监测手环后端服务 - Parkinson's Tremor Monitoring Backend",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 路由注册 (Route Registration)
# ============================================================

# 认证相关
app.include_router(auth.router, prefix="/api/auth", tags=["认证 Authentication"])

# 设备管理
app.include_router(device.router, prefix="/api/device", tags=["设备 Device"])

# 数据上传与查询
app.include_router(data.router, prefix="/api/data", tags=["数据 Data"])

# 震颤分析
app.include_router(analysis.router, prefix="/api/analysis", tags=["分析 Analysis"])

# AI 医生
app.include_router(ai.router, prefix="/api/ai", tags=["AI医生 AI Doctor"])

# 报告生成
app.include_router(report.router, prefix="/api/report", tags=["报告 Report"])

# 测试接口 (ESP32 数据调试)
app.include_router(test.router, prefix="/api/test", tags=["测试 Test"])

# 参数配置接口 (ESP32 震颤检测参数)
app.include_router(config.router, prefix="/api/config", tags=["配置 Config"])


# ============================================================
# API 信息路由 (API Info Route)
# ============================================================

@app.get("/api")
async def api_info():
    """API 根路径 - 服务信息"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "message": "震颤卫士 API 服务正常运行",
        "endpoints": {
            "auth": "/api/auth",
            "device": "/api/device",
            "data": "/api/data",
            "analysis": "/api/analysis",
            "ai": "/api/ai",
            "report": "/api/report"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: 实际检查数据库连接
        "redis": "connected"      # TODO: 实际检查 Redis 连接
    }


# ============================================================
# 前端静态文件服务 (Frontend Static Files)
# 单容器部署时，后端同时服务前端静态文件
# ============================================================

# 检查静态文件目录是否存在（单容器部署时会存在）
if os.path.exists(STATIC_DIR):
    # 挂载静态资源目录 (js, css, images 等)
    # 注意：这个挂载必须在 catch-all 路由之前
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/", response_class=HTMLResponse)
    async def serve_frontend_root():
        """服务前端首页"""
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return HTMLResponse("<h1>Tremor Guard</h1><p>Frontend not built yet.</p>")

    @app.get("/{path:path}")
    async def serve_frontend(path: str, request: Request):
        """
        服务前端静态文件，支持 SPA 路由
        - 如果是静态文件（存在于 static 目录），直接返回
        - 否则返回 index.html（支持 Vue Router History 模式）
        - API 请求不会到达这里（已被前面的路由处理）
        """
        # API 请求不处理
        if path.startswith("api/"):
            return {"error": "Not found"}, 404

        # 尝试返回静态文件
        file_path = os.path.join(STATIC_DIR, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)

        # SPA 路由回退到 index.html
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)

        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)

else:
    # 开发模式或后端独立部署时，只提供 API
    @app.get("/")
    async def root():
        """API 根路径"""
        return {
            "name": settings.APP_NAME,
            "version": "1.0.0",
            "status": "running",
            "message": "震颤卫士 API 服务正常运行 (API Only Mode)",
            "docs": "/docs" if settings.DEBUG else None
        }


# ============================================================
# 启动入口 (Entry Point)
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
