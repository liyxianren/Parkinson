"""
Tremor Guard - Authentication API
震颤卫士 - 认证接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ============================================================
# Pydantic Schemas
# ============================================================

class UserCreate(BaseModel):
    """用户注册"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """用户登录"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT Token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ============================================================
# API Endpoints
# ============================================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册

    - **email**: 邮箱地址
    - **username**: 用户名
    - **password**: 密码
    - **full_name**: 全名 (可选)
    """
    # TODO: 实现用户注册逻辑
    # 1. 检查邮箱/用户名是否已存在
    # 2. 哈希密码
    # 3. 创建用户
    # 4. 返回用户信息
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="注册功能待实现"
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    使用 OAuth2 密码流程
    """
    # TODO: 实现登录逻辑
    # 1. 验证用户名/密码
    # 2. 生成 JWT token
    # 3. 更新最后登录时间
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="登录功能待实现"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户信息"""
    # TODO: 解析 token 并返回用户信息
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """用户登出"""
    # TODO: 实现登出逻辑 (可选: 将 token 加入黑名单)
    return {"message": "登出成功"}


@router.post("/refresh", response_model=Token)
async def refresh_token(token: str = Depends(oauth2_scheme)):
    """刷新 Token"""
    # TODO: 验证并刷新 token
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )
