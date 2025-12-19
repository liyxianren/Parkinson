"""
Tremor Guard - Config API
震颤卫士 - 参数配置接口

用于管理震颤检测参数的云端配置
ESP32 设备可通过 GET /api/config/current 拉取最新配置
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

router = APIRouter()

# ============================================================
# 数据模型 (Data Models)
# ============================================================

class TremorConfig(BaseModel):
    """震颤检测配置参数"""
    # RMS 幅度阈值 (g)
    rms_min: float = Field(default=2.5, ge=0.1, le=10.0, description="RMS 下限阈值 (g)")
    rms_max: float = Field(default=5.0, ge=0.5, le=20.0, description="RMS 上限阈值 (g)")

    # 功率阈值
    power_threshold: float = Field(default=0.5, ge=0.01, le=5.0, description="功率阈值")

    # 频率范围 (Hz)
    freq_min: float = Field(default=4.0, ge=1.0, le=10.0, description="频率下限 (Hz)")
    freq_max: float = Field(default=6.0, ge=2.0, le=15.0, description="频率上限 (Hz)")

    # 严重度分级阈值 (g) - 4个值对应 1-4 级
    severity_thresholds: List[float] = Field(
        default=[2.5, 3.0, 3.5, 4.0],
        min_length=4,
        max_length=4,
        description="严重度分级阈值 [0级, 1级, 2级, 3级]"
    )


class ConfigResponse(BaseModel):
    """配置响应"""
    version: int
    updated_at: str
    params: TremorConfig


class ConfigSaveRequest(BaseModel):
    """保存配置请求"""
    rms_min: Optional[float] = None
    rms_max: Optional[float] = None
    power_threshold: Optional[float] = None
    freq_min: Optional[float] = None
    freq_max: Optional[float] = None
    severity_thresholds: Optional[List[float]] = None


# ============================================================
# 全局配置存储 (Global Config Storage)
# ============================================================

# 默认配置
DEFAULT_CONFIG = TremorConfig()

# 当前配置 (内存存储)
current_config = TremorConfig()
config_version = 1
config_updated_at = datetime.now().isoformat()


# ============================================================
# API 接口 (API Endpoints)
# ============================================================

@router.get("/current", response_model=ConfigResponse)
async def get_current_config():
    """
    获取当前配置

    ESP32 设备通过此接口拉取最新的震颤检测参数
    """
    return ConfigResponse(
        version=config_version,
        updated_at=config_updated_at,
        params=current_config
    )


@router.post("/save")
async def save_config(request: ConfigSaveRequest):
    """
    保存配置参数

    前端调用此接口保存修改后的参数
    只更新提供的字段，未提供的保持原值
    """
    global current_config, config_version, config_updated_at

    # 更新配置 (只更新提供的字段)
    update_data = request.model_dump(exclude_none=True)

    if update_data:
        # 创建新配置
        current_data = current_config.model_dump()
        current_data.update(update_data)
        current_config = TremorConfig(**current_data)

        # 更新版本和时间
        config_version += 1
        config_updated_at = datetime.now().isoformat()

    return {
        "status": "ok",
        "message": "配置已保存",
        "version": config_version,
        "updated_at": config_updated_at
    }


@router.post("/reset")
async def reset_config():
    """
    重置为默认配置
    """
    global current_config, config_version, config_updated_at

    current_config = TremorConfig()
    config_version += 1
    config_updated_at = datetime.now().isoformat()

    return {
        "status": "ok",
        "message": "配置已重置为默认值",
        "version": config_version,
        "updated_at": config_updated_at
    }


@router.get("/defaults")
async def get_default_config():
    """
    获取默认配置值

    用于前端显示默认值参考
    """
    return {
        "params": DEFAULT_CONFIG.model_dump(),
        "description": {
            "rms_min": "RMS 幅度下限阈值 (g) - 低于此值不判定为震颤",
            "rms_max": "RMS 幅度上限阈值 (g) - 高于此值判定为超出范围",
            "power_threshold": "频带功率阈值 - 震颤频段的功率需超过此值",
            "freq_min": "震颤频率下限 (Hz) - 帕金森震颤典型为 4-6Hz",
            "freq_max": "震颤频率上限 (Hz)",
            "severity_thresholds": "严重度分级阈值 (g) - [0级/1级/2级/3级分界点]"
        }
    }


@router.get("/history")
async def get_config_history():
    """
    获取配置变更历史

    TODO: 实现配置历史记录功能
    """
    return {
        "message": "配置历史功能开发中",
        "current_version": config_version
    }
