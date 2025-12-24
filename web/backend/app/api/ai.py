"""
Tremor Guard - AI API
震颤卫士 - AI 分析接口 (Claude)

使用 Anthropic Claude API 提供智能分析和对话功能
"""

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List
import json

from app.core.database import get_db
from app.core.config import settings
from app.api.auth import get_current_user_from_token
from app.models.user import User
from app.models.tremor_data import TremorData, TremorSession

router = APIRouter()

# Claude API 配置
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-3-haiku-20240307"


# ============================================================
# Pydantic Schemas
# ============================================================

class ChatMessage(BaseModel):
    """聊天消息"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    suggestions: List[str]


class AnalysisRequest(BaseModel):
    """分析请求"""
    days: int = 7


class AnalysisResponse(BaseModel):
    """分析响应"""
    summary: str
    key_findings: List[str]
    recommendations: List[str]
    risk_level: str


# ============================================================
# Helper Functions
# ============================================================

async def get_user_data_summary(db: AsyncSession, user_id: int, days: int = 7) -> dict:
    """获取用户数据摘要用于 AI 分析"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 获取会话
    sessions_result = await db.execute(
        select(TremorSession).where(
            and_(
                TremorSession.user_id == user_id,
                TremorSession.start_time >= start_date
            )
        )
    )
    sessions = sessions_result.scalars().all()
    session_ids = [s.id for s in sessions]

    if not session_ids:
        return {
            "has_data": False,
            "days": days,
            "total_sessions": 0,
            "total_analyses": 0,
            "tremor_count": 0,
            "detection_rate": 0,
            "avg_severity": 0,
            "max_severity": 0
        }

    # 统计数据
    stats_result = await db.execute(
        select(
            func.count(TremorData.id).label('total'),
            func.count(TremorData.id).filter(TremorData.detected == True).label('tremor_count'),
            func.avg(TremorData.frequency).filter(TremorData.detected == True).label('avg_freq'),
            func.avg(TremorData.rms_amplitude).label('avg_amp'),
            func.avg(TremorData.severity).filter(TremorData.detected == True).label('avg_sev'),
            func.max(TremorData.severity).label('max_sev')
        ).where(TremorData.session_id.in_(session_ids))
    )
    stats = stats_result.one()

    total = stats.total or 0
    tremor_count = stats.tremor_count or 0
    detection_rate = (tremor_count / total * 100) if total > 0 else 0

    return {
        "has_data": True,
        "days": days,
        "total_sessions": len(sessions),
        "total_analyses": total,
        "tremor_count": tremor_count,
        "detection_rate": round(detection_rate, 1),
        "avg_frequency": round(float(stats.avg_freq), 2) if stats.avg_freq else None,
        "avg_amplitude": round(float(stats.avg_amp), 4) if stats.avg_amp else None,
        "avg_severity": round(float(stats.avg_sev), 2) if stats.avg_sev else 0,
        "max_severity": stats.max_sev or 0
    }


async def call_claude_api(messages: list, system_prompt: str) -> str:
    """调用 Claude API"""
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI 服务未配置，请联系管理员"
        )

    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": messages
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CLAUDE_API_URL,
                headers=headers,
                json=payload,
                timeout=30.0
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"AI 服务响应错误: {response.status_code}"
                )

            result = response.json()
            return result["content"][0]["text"]

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI 服务响应超时"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI 服务错误: {str(e)}"
        )


# ============================================================
# API Endpoints
# ============================================================

@router.post("/chat", response_model=ChatResponse)
async def ai_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    AI 问答助手

    用户可以询问关于震颤数据、帕金森病等问题
    """
    # 获取用户数据摘要
    user_data = await get_user_data_summary(db, current_user.id, 7)

    # 构建系统提示
    system_prompt = f"""你是震颤卫士（Tremor Guard）的 AI 健康助手，专门帮助帕金森病患者理解和管理震颤症状。

用户的最近7天数据摘要:
- 检测会话数: {user_data['total_sessions']}
- 总检测次数: {user_data['total_analyses']}
- 震颤次数: {user_data['tremor_count']}
- 震颤检出率: {user_data['detection_rate']}%
- 平均严重度: {user_data['avg_severity']} (0-4级)
- 最高严重度: {user_data['max_severity']}

你的职责:
1. 帮助用户理解他们的震颤数据
2. 提供关于帕金森病震颤的科普知识
3. 给出日常生活建议（但不能替代医生诊断）
4. 回答用户关于症状管理的问题

重要提醒:
- 始终建议用户咨询专业医生
- 不要做出诊断性陈述
- 用简洁友好的中文回答
- 如果问题超出你的能力范围，坦诚告知"""

    # 构建消息历史
    messages = []
    if request.conversation_history:
        for msg in request.conversation_history[-6:]:  # 保留最近6条消息
            messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": request.message})

    # 调用 Claude API
    response_text = await call_claude_api(messages, system_prompt)

    # 生成建议问题
    suggestions = [
        "我的震颤数据说明什么？",
        "如何减轻震颤症状？",
        "什么时候应该去看医生？"
    ]

    return ChatResponse(
        response=response_text,
        suggestions=suggestions
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def ai_analyze(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    AI 智能分析

    对用户的震颤数据进行深度分析
    """
    # 获取用户数据摘要
    user_data = await get_user_data_summary(db, current_user.id, request.days)

    if not user_data["has_data"]:
        return AnalysisResponse(
            summary="暂无足够的数据进行分析。请确保设备正常连接并进行几次检测后再试。",
            key_findings=["尚未检测到足够的数据"],
            recommendations=["确保设备已正确佩戴", "尝试进行几次检测会话"],
            risk_level="未知"
        )

    # 构建分析提示
    system_prompt = """你是一个专业的帕金森病震颤数据分析助手。
请基于提供的数据给出专业、准确的分析报告。
回复必须是有效的 JSON 格式，包含以下字段:
- summary: 一段总结性文字（100-200字）
- key_findings: 关键发现数组（3-5项）
- recommendations: 建议数组（3-5项）
- risk_level: 风险等级（"低"、"中"、"高" 之一）

注意：不要做医学诊断，只分析数据趋势。"""

    analysis_prompt = f"""请分析以下震颤检测数据（最近{request.days}天）:

检测统计:
- 检测会话数: {user_data['total_sessions']}
- 总检测次数: {user_data['total_analyses']}
- 震颤次数: {user_data['tremor_count']}
- 震颤检出率: {user_data['detection_rate']}%

震颤特征:
- 平均严重度: {user_data['avg_severity']} (0=无震颤, 1=轻度, 2=中轻度, 3=中度, 4=重度)
- 最高严重度: {user_data['max_severity']}
- 平均频率: {user_data.get('avg_frequency', '未知')} Hz
- 平均振幅: {user_data.get('avg_amplitude', '未知')} g

请给出分析报告（JSON格式）:"""

    messages = [{"role": "user", "content": analysis_prompt}]

    try:
        response_text = await call_claude_api(messages, system_prompt)

        # 解析 JSON 响应
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            analysis_result = json.loads(json_str)

            return AnalysisResponse(
                summary=analysis_result.get("summary", "分析完成"),
                key_findings=analysis_result.get("key_findings", []),
                recommendations=analysis_result.get("recommendations", []),
                risk_level=analysis_result.get("risk_level", "中")
            )
        else:
            return AnalysisResponse(
                summary=response_text[:500],
                key_findings=["AI 分析已完成"],
                recommendations=["建议定期监测", "如有异常请咨询医生"],
                risk_level="中"
            )

    except json.JSONDecodeError:
        return AnalysisResponse(
            summary="分析完成，但结果格式解析失败。",
            key_findings=["数据已收集"],
            recommendations=["建议定期监测", "如有异常请咨询医生"],
            risk_level="中"
        )


@router.get("/insights")
async def get_ai_insights(
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db),
    days: int = 7
):
    """
    获取 AI 洞察

    自动生成近期数据的关键洞察
    """
    user_data = await get_user_data_summary(db, current_user.id, days)

    if not user_data["has_data"]:
        return {
            "insights": ["开始监测后将生成数据洞察"],
            "generated_at": datetime.utcnow(),
            "period_days": days
        }

    insights = []

    if user_data["detection_rate"] > 50:
        insights.append(f"最近{days}天震颤检出率较高（{user_data['detection_rate']}%），建议关注")
    elif user_data["detection_rate"] < 20:
        insights.append(f"最近{days}天震颤检出率较低（{user_data['detection_rate']}%），状态良好")

    if user_data["avg_severity"] >= 2:
        insights.append(f"平均严重度为 {user_data['avg_severity']}，建议咨询医生")
    elif user_data["avg_severity"] > 0:
        insights.append(f"平均严重度为 {user_data['avg_severity']}，属于轻度范围")

    if user_data["max_severity"] >= 3:
        insights.append(f"检测到最高严重度 {user_data['max_severity']}，请注意观察")

    if user_data["total_sessions"] > 0:
        insights.append(f"共完成 {user_data['total_sessions']} 次检测会话")

    if not insights:
        insights.append("数据正常，继续保持监测习惯")

    return {
        "insights": insights,
        "generated_at": datetime.utcnow(),
        "period_days": days,
        "data_summary": user_data
    }


@router.get("/health-tips")
async def get_health_tips(
    current_user: User = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_db)
):
    """
    获取健康提示

    基于用户数据生成个性化健康建议
    """
    user_data = await get_user_data_summary(db, current_user.id, 7)

    tips = [
        "保持规律作息有助于减轻震颤症状",
        "适度运动可以改善运动功能",
        "避免过度疲劳和压力"
    ]

    personalized = False
    if user_data["has_data"]:
        personalized = True
        if user_data["avg_severity"] >= 2:
            tips.insert(0, "您的震颤症状需要关注，建议咨询医生调整治疗方案")
        if user_data["detection_rate"] > 40:
            tips.insert(0, "震颤较为频繁，建议记录发作时间和环境因素")

    return {
        "tips": tips,
        "personalized": personalized,
        "generated_at": datetime.utcnow()
    }
