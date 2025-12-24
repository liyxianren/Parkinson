/**
 * Tremor Guard - AI API
 * 震颤卫士 - AI API
 */

import apiClient from './index'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  message: string
  conversation_history?: ChatMessage[]
}

export interface ChatResponse {
  response: string
  suggestions: string[]
}

export interface AnalysisResponse {
  summary: string
  key_findings: string[]
  recommendations: string[]
  risk_level: string
}

export interface InsightsResponse {
  insights: string[]
  generated_at: string
  period_days: number
  data_summary?: Record<string, unknown>
}

export interface HealthTipsResponse {
  tips: string[]
  personalized: boolean
  generated_at: string
}

export const aiApi = {
  /**
   * AI 对话
   */
  async chat(message: string, history?: ChatMessage[]): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/ai/chat', {
      message,
      conversation_history: history
    })
    return response.data
  },

  /**
   * AI 分析
   */
  async analyze(days = 7): Promise<AnalysisResponse> {
    const response = await apiClient.post<AnalysisResponse>('/ai/analyze', {
      days
    })
    return response.data
  },

  /**
   * 获取洞察
   */
  async getInsights(days = 7): Promise<InsightsResponse> {
    const response = await apiClient.get<InsightsResponse>('/ai/insights', {
      params: { days }
    })
    return response.data
  },

  /**
   * 获取健康提示
   */
  async getHealthTips(): Promise<HealthTipsResponse> {
    const response = await apiClient.get<HealthTipsResponse>('/ai/health-tips')
    return response.data
  }
}
