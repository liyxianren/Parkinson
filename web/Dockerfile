# ========================================
# Tremor Guard - 单容器部署 Dockerfile
# 震颤卫士 - 前后端合一，只需部署一个服务
# ========================================
# 参考: naicha 项目的 Docker 配置
# ========================================

# ============ 第一阶段：构建前端 ============
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund

# 复制前端源代码
COPY frontend ./

# 构建前端（API 地址使用相对路径，由后端统一提供）
ENV VITE_API_BASE_URL=/api
RUN npm run build

# ============ 第二阶段：构建后端并整合前端 ============
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 安装系统依赖 (WeasyPrint PDF 生成需要)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend ./

# 从第一阶段复制前端构建产物到静态目录
COPY --from=frontend-builder /app/frontend/dist ./static

# 环境变量 (Zeabur 会自动设置 PORT)
ENV APP_ENV=production \
    DEBUG=false \
    PORT=8000 \
    HOST=0.0.0.0

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# 启动 FastAPI（会自动服务 static 目录的前端文件）
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
