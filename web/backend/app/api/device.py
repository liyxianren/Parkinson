"""
Tremor Guard - Device API
震颤卫士 - 设备管理接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from app.core.database import get_db
from app.api.auth import oauth2_scheme

router = APIRouter()


# ============================================================
# Pydantic Schemas
# ============================================================

class DeviceRegister(BaseModel):
    """设备注册"""
    device_id: str  # 硬件唯一ID
    name: Optional[str] = None
    firmware_version: Optional[str] = None
    hardware_version: Optional[str] = None
    mac_address: Optional[str] = None


class DeviceUpdate(BaseModel):
    """设备更新"""
    name: Optional[str] = None
    is_online: Optional[bool] = None
    battery_level: Optional[float] = None


class DeviceResponse(BaseModel):
    """设备响应"""
    id: int
    device_id: str
    name: Optional[str]
    firmware_version: Optional[str]
    is_online: bool
    battery_level: Optional[float]
    last_seen: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceHeartbeat(BaseModel):
    """设备心跳"""
    device_id: str
    battery_level: Optional[float] = None
    firmware_version: Optional[str] = None


# ============================================================
# API Endpoints
# ============================================================

@router.post("/register", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(
    device_data: DeviceRegister,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    注册新设备

    将设备绑定到当前用户账户
    """
    # TODO: 实现设备注册
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )


@router.get("/list", response_model=List[DeviceResponse])
async def list_devices(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的所有设备"""
    # TODO: 查询用户设备列表
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: str,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """获取设备详情"""
    # TODO: 查询设备信息
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: str,
    device_data: DeviceUpdate,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """更新设备信息"""
    # TODO: 更新设备
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """删除设备绑定"""
    # TODO: 解绑设备
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能待实现"
    )


@router.post("/heartbeat")
async def device_heartbeat(
    heartbeat: DeviceHeartbeat,
    db: AsyncSession = Depends(get_db)
):
    """
    设备心跳

    设备定期调用此接口报告在线状态
    """
    # TODO: 更新设备在线状态和最后在线时间
    return {"status": "ok", "timestamp": datetime.utcnow()}
