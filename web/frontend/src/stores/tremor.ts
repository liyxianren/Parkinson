/**
 * Tremor Guard - Tremor Data Store
 * 震颤卫士 - 震颤数据状态管理
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { TremorData, TremorSession, DailyStats } from '@/types'

export const useTremorStore = defineStore('tremor', () => {
  // State
  const currentSession = ref<TremorSession | null>(null)
  const recentData = ref<TremorData[]>([])
  const sessions = ref<TremorSession[]>([])
  const dailyStats = ref<DailyStats | null>(null)
  const loading = ref(false)

  // Getters
  const isMonitoring = computed(() => currentSession.value?.is_active ?? false)

  const latestReading = computed(() => {
    if (recentData.value.length === 0) return null
    return recentData.value[recentData.value.length - 1]
  })

  const tremorDetectionRate = computed(() => {
    if (recentData.value.length === 0) return 0
    const detections = recentData.value.filter(d => d.detected).length
    return (detections / recentData.value.length) * 100
  })

  const averageSeverity = computed(() => {
    const detected = recentData.value.filter(d => d.detected)
    if (detected.length === 0) return 0
    const sum = detected.reduce((acc, d) => acc + d.severity, 0)
    return sum / detected.length
  })

  // Actions
  function addReading(data: TremorData) {
    recentData.value.push(data)
    // 保持最近 100 条数据
    if (recentData.value.length > 100) {
      recentData.value.shift()
    }
  }

  function clearRecentData() {
    recentData.value = []
  }

  function setCurrentSession(session: TremorSession | null) {
    currentSession.value = session
  }

  async function fetchSessions(limit = 20) {
    loading.value = true
    try {
      // TODO: 调用 API 获取会话列表
      // sessions.value = await dataApi.getSessions(limit)
    } finally {
      loading.value = false
    }
  }

  async function fetchDailyStats(date?: Date) {
    loading.value = true
    try {
      // TODO: 调用 API 获取每日统计
      // dailyStats.value = await analysisApi.getDailyStats(date)
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    currentSession,
    recentData,
    sessions,
    dailyStats,
    loading,

    // Getters
    isMonitoring,
    latestReading,
    tremorDetectionRate,
    averageSeverity,

    // Actions
    addReading,
    clearRecentData,
    setCurrentSession,
    fetchSessions,
    fetchDailyStats,
  }
})
