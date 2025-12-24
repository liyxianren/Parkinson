<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useTremorStore } from '@/stores/tremor'
import { getSeverityLabel, getSeverityColor } from '@/types'
import AppLayout from '@/layouts/AppLayout.vue'
import type { TremorData } from '@/types'
import { dataApi } from '@/api/data'

const tremorStore = useTremorStore()

// 状态
const loading = ref(false)
const error = ref<string | null>(null)
const deviceId = ref('ESP32_DEFAULT')

// 图表数据
const chartData = ref<{ time: string; amplitude: number; severity: number }[]>([])
const maxChartPoints = 60

// 自动刷新
const refreshInterval = ref<number | null>(null)
const refreshRate = 2000 // 2秒刷新一次

// 计算属性
const isMonitoring = computed(() => tremorStore.currentSession?.is_active ?? false)
const currentSession = computed(() => tremorStore.currentSession)
const recentData = computed(() => tremorStore.recentData)
const latestReading = computed(() => tremorStore.latestReading)

const sessionStats = computed(() => {
  if (!currentSession.value) {
    return {
      totalAnalyses: 0,
      tremorCount: 0,
      detectionRate: 0,
      avgSeverity: 0,
      maxSeverity: 0,
      duration: 0
    }
  }
  const session = currentSession.value
  return {
    totalAnalyses: session.total_analyses,
    tremorCount: session.tremor_count,
    detectionRate: session.total_analyses > 0
      ? ((session.tremor_count / session.total_analyses) * 100).toFixed(1)
      : 0,
    avgSeverity: session.avg_severity?.toFixed(2) || 0,
    maxSeverity: session.max_severity,
    duration: session.duration_seconds || 0
  }
})

const currentSeverity = computed(() => {
  if (!latestReading.value || !latestReading.value.detected) return 0
  return latestReading.value.severity
})

const currentFrequency = computed(() => {
  if (!latestReading.value) return null
  return latestReading.value.frequency
})

const currentAmplitude = computed(() => {
  if (!latestReading.value) return null
  return latestReading.value.rms_amplitude
})

// 方法
async function startMonitoring() {
  loading.value = true
  error.value = null

  try {
    await tremorStore.startSession(deviceId.value)
    tremorStore.clearRecentData()
    chartData.value = []
    startAutoRefresh()
  } catch (e: any) {
    error.value = e.response?.data?.detail || '启动监测失败'
  } finally {
    loading.value = false
  }
}

async function stopMonitoring() {
  if (!currentSession.value) return

  loading.value = true
  error.value = null

  try {
    stopAutoRefresh()
    await tremorStore.endSession(currentSession.value.id)
  } catch (e: any) {
    error.value = e.response?.data?.detail || '停止监测失败'
  } finally {
    loading.value = false
  }
}

function toggleMonitoring() {
  if (isMonitoring.value) {
    stopMonitoring()
  } else {
    startMonitoring()
  }
}

async function refreshData() {
  if (!currentSession.value) return

  try {
    const session = await dataApi.getSession(currentSession.value.id)
    tremorStore.setCurrentSession(session)

    const data = await dataApi.getSessionData(currentSession.value.id, 50)
    tremorStore.recentData = data

    updateChartData(data)
  } catch (e) {
    console.error('刷新数据失败:', e)
  }
}

function updateChartData(data: TremorData[]) {
  const newPoints = data
    .slice()
    .reverse()
    .map(d => ({
      time: formatTime(d.timestamp),
      amplitude: d.rms_amplitude || 0,
      severity: d.severity
    }))
    .slice(-maxChartPoints)

  chartData.value = newPoints
}

function startAutoRefresh() {
  if (refreshInterval.value) return
  refreshInterval.value = window.setInterval(refreshData, refreshRate)
}

function stopAutoRefresh() {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

function formatTime(dateStr: string) {
  return new Date(dateStr).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

function formatDuration(seconds: number) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 生命周期
onMounted(async () => {
  try {
    const sessions = await dataApi.getHistory({ limit: 1 })
    const activeSession = sessions.find(s => s.is_active)
    if (activeSession) {
      tremorStore.setCurrentSession(activeSession)
      await refreshData()
      startAutoRefresh()
    }
  } catch (e) {
    console.error('获取会话失败:', e)
  }
})

onUnmounted(() => {
  stopAutoRefresh()
})

watch(isMonitoring, (newVal) => {
  if (newVal) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
})
</script>

<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- 页面标题 -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">实时监测</h1>
          <p class="text-gray-500 mt-1">实时查看震颤检测数据</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="badge" :class="isMonitoring ? 'badge-success' : 'bg-warmGray-200 text-gray-600'">
            <span v-if="isMonitoring" class="w-2 h-2 bg-mint-500 rounded-full animate-pulse mr-1.5"></span>
            {{ isMonitoring ? '监测中' : '待机' }}
          </span>
        </div>
      </div>

      <!-- 错误提示 -->
      <Transition name="fade-up">
        <div v-if="error" class="alert alert-error">
          <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="flex-1">{{ error }}</span>
          <button @click="error = null" class="btn btn-ghost btn-sm !p-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </Transition>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左侧：控制面板 + 当前状态 -->
        <div class="space-y-6">
          <!-- 控制面板 -->
          <div class="card text-center !p-8">
            <!-- 监测状态圆环 -->
            <div class="relative w-40 h-40 mx-auto mb-6">
              <!-- 外层光环 -->
              <div
                v-if="isMonitoring"
                class="absolute inset-0 rounded-full border-4 border-mint-400 animate-pulse-ring"
              ></div>
              <div
                v-if="isMonitoring"
                class="absolute inset-0 rounded-full border-4 border-mint-400 animate-pulse-ring"
                style="animation-delay: 1s;"
              ></div>

              <!-- 主圆环 -->
              <div
                class="absolute inset-4 rounded-full flex items-center justify-center transition-all duration-500"
                :class="isMonitoring
                  ? 'bg-gradient-to-br from-mint-400 to-mint-500 shadow-glow'
                  : 'bg-warmGray-100'"
              >
                <svg
                  class="w-16 h-16 transition-colors"
                  :class="isMonitoring ? 'text-white' : 'text-warmGray-400'"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>

            <h2 class="text-2xl font-bold text-gray-800 mb-2">
              {{ isMonitoring ? '监测进行中' : '准备就绪' }}
            </h2>
            <p class="text-gray-500 mb-8">
              {{ isMonitoring ? '正在实时接收设备数据' : '点击下方按钮开始震颤监测' }}
            </p>

            <button
              @click="toggleMonitoring"
              :disabled="loading"
              class="btn btn-lg w-full"
              :class="isMonitoring ? 'btn-danger' : 'btn-primary'"
            >
              <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <span v-if="loading">处理中...</span>
              <template v-else>
                <svg v-if="!isMonitoring" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                </svg>
                <span>{{ isMonitoring ? '停止监测' : '开始监测' }}</span>
              </template>
            </button>

            <p class="text-sm text-gray-400 mt-4 flex items-center justify-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              设备: {{ deviceId }}
            </p>
          </div>

          <!-- 当前严重度 -->
          <div class="card">
            <h3 class="text-lg font-bold text-gray-800 mb-4">当前状态</h3>

            <div class="text-center mb-6">
              <div
                class="w-28 h-28 rounded-full mx-auto flex items-center justify-center text-4xl font-bold text-white shadow-soft transition-all duration-300"
                :style="{ backgroundColor: getSeverityColor(currentSeverity) }"
              >
                {{ currentSeverity }}
              </div>
              <p class="mt-4 text-lg font-semibold" :style="{ color: getSeverityColor(currentSeverity) }">
                {{ getSeverityLabel(currentSeverity) }}
              </p>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="card-flat !p-4 text-center">
                <p class="text-sm text-gray-500 mb-1">频率</p>
                <p class="text-xl font-bold text-gray-800">
                  {{ currentFrequency ? `${currentFrequency.toFixed(2)}` : '-' }}
                  <span class="text-sm font-normal text-gray-500">Hz</span>
                </p>
              </div>
              <div class="card-flat !p-4 text-center">
                <p class="text-sm text-gray-500 mb-1">振幅</p>
                <p class="text-xl font-bold text-gray-800">
                  {{ currentAmplitude ? `${currentAmplitude.toFixed(3)}` : '-' }}
                  <span class="text-sm font-normal text-gray-500">g</span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：图表 + 数据列表 -->
        <div class="lg:col-span-2 space-y-6">
          <!-- 会话统计 -->
          <Transition name="fade-up">
            <div v-if="isMonitoring" class="card-gradient">
              <h3 class="text-lg font-bold text-gray-800 mb-4">会话统计</h3>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="text-center p-4 bg-white/50 rounded-xl">
                  <p class="text-sm text-gray-500 mb-1">持续时间</p>
                  <p class="text-2xl font-bold text-gray-800">{{ formatDuration(sessionStats.duration) }}</p>
                </div>
                <div class="text-center p-4 bg-white/50 rounded-xl">
                  <p class="text-sm text-gray-500 mb-1">检测次数</p>
                  <p class="text-2xl font-bold text-primary-600">{{ sessionStats.totalAnalyses }}</p>
                </div>
                <div class="text-center p-4 bg-white/50 rounded-xl">
                  <p class="text-sm text-gray-500 mb-1">震颤次数</p>
                  <p class="text-2xl font-bold text-orange-500">{{ sessionStats.tremorCount }}</p>
                </div>
                <div class="text-center p-4 bg-white/50 rounded-xl">
                  <p class="text-sm text-gray-500 mb-1">检出率</p>
                  <p class="text-2xl font-bold text-gray-800">{{ sessionStats.detectionRate }}%</p>
                </div>
              </div>
            </div>
          </Transition>

          <!-- 波形图 -->
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-bold text-gray-800">振幅趋势</h3>
              <span class="badge badge-primary">实时</span>
            </div>
            <div class="h-52 relative bg-warmGray-50 rounded-xl p-4">
              <div v-if="chartData.length === 0" class="absolute inset-0 flex items-center justify-center">
                <div class="text-center text-gray-400">
                  <div class="w-16 h-16 bg-warmGray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                  <p>等待数据...</p>
                </div>
              </div>

              <!-- 简易条形图 -->
              <div v-else class="h-full flex items-end gap-0.5">
                <div
                  v-for="(point, index) in chartData"
                  :key="index"
                  class="flex-1 rounded-t-sm transition-all duration-200"
                  :style="{
                    height: `${Math.min(100, Math.max(5, point.amplitude * 500))}%`,
                    backgroundColor: getSeverityColor(point.severity)
                  }"
                  :title="`${point.time}: ${point.amplitude.toFixed(3)}g`"
                ></div>
              </div>
            </div>
          </div>

          <!-- 最近数据列表 -->
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-bold text-gray-800">最近检测记录</h3>
              <span class="text-sm text-gray-500">共 {{ recentData.length }} 条</span>
            </div>

            <div class="table-container !shadow-none">
              <table class="table">
                <thead>
                  <tr>
                    <th>时间</th>
                    <th>状态</th>
                    <th>频率</th>
                    <th>振幅</th>
                    <th>严重度</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(data, index) in recentData.slice(0, 10)"
                    :key="data.id"
                    class="animate-fade-in-up"
                    :style="{ animationDelay: `${index * 30}ms` }"
                  >
                    <td class="font-medium">{{ formatTime(data.timestamp) }}</td>
                    <td>
                      <span
                        :class="[
                          'badge',
                          data.detected ? 'badge-warning' : 'badge-success'
                        ]"
                      >
                        {{ data.detected ? '震颤' : '正常' }}
                      </span>
                    </td>
                    <td>{{ data.frequency?.toFixed(2) || '-' }} Hz</td>
                    <td>{{ data.rms_amplitude?.toFixed(3) || '-' }} g</td>
                    <td>
                      <span class="severity-badge" :class="`severity-${data.severity}`">
                        {{ getSeverityLabel(data.severity) }}
                      </span>
                    </td>
                  </tr>
                  <tr v-if="recentData.length === 0">
                    <td colspan="5" class="!py-12 text-center">
                      <div class="text-gray-400">
                        <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                        </svg>
                        <p>暂无数据</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.animate-pulse-ring {
  animation: pulseRing 2s ease-out infinite;
}

@keyframes pulseRing {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}
</style>
