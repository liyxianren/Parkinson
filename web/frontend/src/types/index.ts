/**
 * Tremor Guard - TypeScript Types
 * 震颤卫士 - 类型定义
 */

// ============================================================
// User Types
// ============================================================

export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role: 'user' | 'doctor' | 'admin'
  is_active: boolean
  is_verified: boolean
  created_at: string
  last_login?: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// ============================================================
// Device Types
// ============================================================

export interface Device {
  id: number
  device_id: string
  name?: string
  firmware_version?: string
  hardware_version?: string
  mac_address?: string
  is_online: boolean
  battery_level?: number
  last_seen?: string
  created_at: string
}

// ============================================================
// Tremor Data Types
// ============================================================

export interface TremorData {
  id: number
  session_id: number
  timestamp: string
  detected: boolean
  valid: boolean
  out_of_range: boolean
  frequency?: number
  peak_power?: number
  band_power?: number
  amplitude?: number
  rms_amplitude?: number
  severity: number
  severity_label?: string
}

export interface TremorSession {
  id: number
  user_id: number
  device_id: number
  start_time: string
  end_time?: string
  duration_seconds?: number
  total_analyses: number
  tremor_count: number
  avg_frequency?: number
  avg_amplitude?: number
  max_severity: number
  avg_severity?: number
  is_active: boolean
}

// ============================================================
// Analysis Types
// ============================================================

export interface DailyStats {
  date: string
  total_sessions: number
  total_analyses: number
  tremor_detections: number
  detection_rate: number
  avg_frequency?: number
  avg_amplitude?: number
  avg_severity?: number
  max_severity: number
}

export interface SeverityDistribution {
  level_0: number
  level_1: number
  level_2: number
  level_3: number
  level_4: number
  total: number
}

export interface WeeklyTrend {
  week_start: string
  week_end: string
  daily_stats: DailyStats[]
  overall_detection_rate: number
  severity_trend: 'improving' | 'stable' | 'worsening'
}

// ============================================================
// AI Types
// ============================================================

export interface AIAnalysisResponse {
  analysis_id: string
  timestamp: string
  analysis_type: string
  summary: string
  detailed_analysis: string
  key_findings: string[]
  recommendations: string[]
  risk_assessment: string
  confidence_score: number
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

// ============================================================
// Report Types
// ============================================================

export type ReportFormat = 'pdf' | 'json' | 'csv'
export type ReportType = 'daily' | 'weekly' | 'monthly' | 'custom'

export interface ReportMetadata {
  report_id: string
  report_type: ReportType
  format: ReportFormat
  generated_at: string
  period_start: string
  period_end: string
  file_size?: number
  download_url?: string
}

// ============================================================
// Severity Helpers
// ============================================================

export const SEVERITY_LABELS: Record<number, string> = {
  0: '无震颤',
  1: '轻度',
  2: '中轻度',
  3: '中度',
  4: '重度',
}

export const SEVERITY_COLORS: Record<number, string> = {
  0: '#10b981', // green
  1: '#84cc16', // lime
  2: '#eab308', // yellow
  3: '#f97316', // orange
  4: '#ef4444', // red
}

export function getSeverityLabel(severity: number): string {
  return SEVERITY_LABELS[severity] || '未知'
}

export function getSeverityColor(severity: number): string {
  return SEVERITY_COLORS[severity] || '#6b7280'
}
