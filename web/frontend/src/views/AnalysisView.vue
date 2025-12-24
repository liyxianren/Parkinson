<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getSeverityLabel, getSeverityColor, SEVERITY_COLORS } from '@/types'
import AppLayout from '@/layouts/AppLayout.vue'
import { analysisApi, type AnalysisSummary, type TrendDataPoint, type WeeklyTrend } from '@/api/analysis'

// 状态
const loading = ref(true)
const error = ref<string | null>(null)
const selectedDays = ref(7)

// 数据
const summary = ref<AnalysisSummary | null>(null)
const trendData = ref<TrendDataPoint[]>([])
const weeklyTrend = ref<WeeklyTrend | null>(null)

// 时间范围选项
const timeRangeOptions = [
  { label: '最近7天', value: 7 },
  { label: '最近14天', value: 14 },
  { label: '最近30天', value: 30 },
  { label: '最近90天', value: 90 }
]

// 计算属性
const severityDistributionData = computed(() => {
  if (!summary.value) return []
  const dist = summary.value.severity_distribution
  return [
    { level: 0, label: '无震颤', count: dist.level_0, color: SEVERITY_COLORS[0] },
    { level: 1, label: '轻度', count: dist.level_1, color: SEVERITY_COLORS[1] },
    { level: 2, label: '中轻度', count: dist.level_2, color: SEVERITY_COLORS[2] },
    { level: 3, label: '中度', count: dist.level_3, color: SEVERITY_COLORS[3] },
    { level: 4, label: '重度', count: dist.level_4, color: SEVERITY_COLORS[4] }
  ]
})

const maxSeverityCount = computed(() => {
  return Math.max(...severityDistributionData.value.map(d => d.count), 1)
})

const hourlyPeakHours = computed(() => {
  if (!summary.value?.hourly_distribution) return []
  return [...summary.value.hourly_distribution]
    .sort((a, b) => b.tremor_count - a.tremor_count)
    .slice(0, 3)
    .filter(h => h.tremor_count > 0)
})

const trendSeverityTrend = computed(() => {
  if (weeklyTrend.value) {
    return weeklyTrend.value.severity_trend
  }
  return 'stable'
})

const trendLabel = computed(() => {
  switch (trendSeverityTrend.value) {
    case 'improving': return { text: '好转中', color: 'text-mint-600', bg: 'bg-mint-100', icon: 'up' }
    case 'worsening': return { text: '需关注', color: 'text-red-500', bg: 'bg-red-100', icon: 'down' }
    default: return { text: '稳定', color: 'text-gray-600', bg: 'bg-warmGray-100', icon: 'stable' }
  }
})

// 方法
async function loadData() {
  loading.value = true
  error.value = null

  try {
    const [summaryData, trend, weekly] = await Promise.all([
      analysisApi.getSummary(selectedDays.value),
      analysisApi.getTrend(selectedDays.value),
      analysisApi.getWeeklyTrend(0)
    ])

    summary.value = summaryData
    trendData.value = trend
    weeklyTrend.value = weekly
  } catch (e: any) {
    error.value = e.response?.data?.detail || '加载数据失败'
  } finally {
    loading.value = false
  }
}

function formatHour(hour: number): string {
  return `${hour.toString().padStart(2, '0')}:00`
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

function getMaxTrendValue(): number {
  if (trendData.value.length === 0) return 100
  return Math.max(...trendData.value.map(d => d.detection_rate), 10)
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<template>
  <AppLayout>
    <!-- 页面标题 -->
    <div class="mb-8 flex flex-wrap items-start justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl flex items-center justify-center shadow-soft">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-800">数据分析</h1>
          <p class="text-gray-500 text-sm">震颤检测数据统计与趋势分析</p>
        </div>
      </div>

      <!-- 时间范围选择 -->
      <div class="flex items-center gap-3 bg-white rounded-xl px-4 py-2 shadow-soft border border-warmGray-200">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <select
          v-model="selectedDays"
          @change="loadData"
          class="bg-transparent border-none text-sm font-medium text-gray-700 focus:outline-none cursor-pointer"
        >
          <option v-for="opt in timeRangeOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- 错误提示 -->
    <Transition name="fade-up">
      <div v-if="error" class="alert alert-error mb-6">
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ error }}</span>
        <button @click="loadData" class="ml-auto text-red-600 hover:text-red-700 font-medium">重试</button>
      </div>
    </Transition>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex flex-col items-center justify-center h-64">
      <div class="relative">
        <div class="w-16 h-16 border-4 border-primary-200 rounded-full"></div>
        <div class="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin absolute inset-0"></div>
      </div>
      <p class="text-gray-500 mt-4">加载分析数据...</p>
    </div>

    <template v-else-if="summary">
      <!-- 概览卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- 总检测次数 -->
        <div class="card card-gradient group">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-gray-500 text-sm mb-1">检测次数</p>
              <p class="text-3xl font-bold text-gray-800">{{ summary.total_analyses.toLocaleString() }}</p>
              <p class="text-xs text-gray-400 mt-2 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                {{ summary.total_sessions }} 次会话
              </p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl flex items-center justify-center shadow-soft group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- 震颤检出率 -->
        <div class="card card-gradient group">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-gray-500 text-sm mb-1">震颤检出率</p>
              <p class="text-3xl font-bold text-amber-600">{{ summary.detection_rate }}%</p>
              <p class="text-xs text-gray-400 mt-2 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                {{ summary.tremor_detections }} 次震颤
              </p>
            </div>
            <div class="w-12 h-12 bg-gradient-to-br from-amber-400 to-amber-600 rounded-xl flex items-center justify-center shadow-soft group-hover:scale-110 transition-transform">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- 平均严重度 -->
        <div class="card card-gradient group">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-gray-500 text-sm mb-1">平均严重度</p>
              <p class="text-3xl font-bold text-gray-800">{{ summary.avg_severity.toFixed(2) }}</p>
              <p class="text-xs mt-2">
                <span class="severity-badge text-xs" :class="`severity-${summary.max_severity}`">
                  最高 {{ getSeverityLabel(summary.max_severity) }}
                </span>
              </p>
            </div>
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center shadow-soft group-hover:scale-110 transition-transform"
              :style="{ background: `linear-gradient(135deg, ${getSeverityColor(Math.round(summary.avg_severity))}90, ${getSeverityColor(Math.round(summary.avg_severity))})`}"
            >
              <span class="text-lg font-bold text-white">
                {{ Math.round(summary.avg_severity) }}
              </span>
            </div>
          </div>
        </div>

        <!-- 趋势状态 -->
        <div class="card card-gradient group">
          <div class="flex items-start justify-between">
            <div>
              <p class="text-gray-500 text-sm mb-1">整体趋势</p>
              <p class="text-2xl font-bold" :class="trendLabel.color">
                {{ trendLabel.text }}
              </p>
              <p class="text-xs text-gray-400 mt-2">
                基于最近一周数据
              </p>
            </div>
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center shadow-soft group-hover:scale-110 transition-transform"
              :class="trendLabel.bg"
            >
              <svg v-if="trendSeverityTrend === 'improving'" class="w-6 h-6 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <svg v-else-if="trendSeverityTrend === 'worsening'" class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
              </svg>
              <svg v-else class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- 严重度分布 -->
        <div class="card">
          <div class="flex items-center gap-2 mb-6">
            <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">严重度分布</h3>
          </div>

          <div class="space-y-4">
            <div
              v-for="(item, index) in severityDistributionData"
              :key="item.level"
              class="flex items-center gap-4 animate-fade-in-up"
              :style="{ animationDelay: `${index * 50}ms` }"
            >
              <div class="w-16 text-sm font-medium text-gray-600">{{ item.label }}</div>
              <div class="flex-1 h-8 bg-warmGray-100 rounded-full overflow-hidden relative">
                <div
                  class="h-full rounded-full transition-all duration-700 ease-out flex items-center justify-end pr-3"
                  :style="{
                    width: `${Math.max((item.count / maxSeverityCount) * 100, item.count > 0 ? 10 : 0)}%`,
                    backgroundColor: item.color
                  }"
                >
                  <span v-if="item.count > 0 && (item.count / maxSeverityCount) > 0.15" class="text-xs font-medium text-white">
                    {{ item.count }}
                  </span>
                </div>
                <span
                  v-if="item.count > 0 && (item.count / maxSeverityCount) <= 0.15"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-medium text-gray-600"
                >
                  {{ item.count }}
                </span>
              </div>
            </div>
          </div>

          <div class="mt-6 pt-4 border-t border-warmGray-200">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">总计</span>
              <span class="font-semibold text-gray-800">{{ summary.severity_distribution.total.toLocaleString() }} 次检测</span>
            </div>
          </div>
        </div>

        <!-- 时段分析 -->
        <div class="card">
          <div class="flex items-center gap-2 mb-6">
            <div class="w-8 h-8 bg-lavender-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-lavender-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">时段分析</h3>
          </div>

          <!-- 高发时段 -->
          <div v-if="hourlyPeakHours.length > 0" class="mb-6">
            <p class="text-sm text-gray-500 mb-3">震颤高发时段</p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(h, index) in hourlyPeakHours"
                :key="h.hour"
                class="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-amber-50 to-amber-100 text-amber-700 rounded-xl text-sm font-medium border border-amber-200 animate-fade-in-up"
                :style="{ animationDelay: `${index * 100}ms` }"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ formatHour(h.hour) }}
                <span class="bg-amber-200 px-1.5 py-0.5 rounded text-xs">{{ h.tremor_count }}次</span>
              </span>
            </div>
          </div>
          <div v-else class="mb-6 flex items-center gap-2 text-gray-400 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            暂无震颤记录
          </div>

          <!-- 24小时分布图 -->
          <div class="bg-warmGray-50 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-3">24小时分布</p>
            <div class="h-32 flex items-end gap-0.5">
              <div
                v-for="(h, index) in summary.hourly_distribution"
                :key="h.hour"
                class="flex-1 rounded-t-lg transition-all duration-300 group relative cursor-pointer hover:opacity-80"
                :style="{
                  height: `${Math.max(8, (h.tremor_count / Math.max(...summary.hourly_distribution.map(x => x.tremor_count), 1)) * 100)}%`,
                  backgroundColor: h.tremor_count > 0 ? getSeverityColor(Math.round(h.avg_severity)) : '#E5E7EB',
                  animationDelay: `${index * 20}ms`
                }"
              >
                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none z-10 shadow-lg">
                  <div class="font-medium">{{ formatHour(h.hour) }}</div>
                  <div class="text-gray-300">{{ h.tremor_count }} 次震颤</div>
                  <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                    <div class="border-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex justify-between text-xs text-gray-400 mt-2 px-1">
              <span>00:00</span>
              <span>06:00</span>
              <span>12:00</span>
              <span>18:00</span>
              <span>24:00</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 趋势图表 -->
      <div class="card mb-8">
        <div class="flex items-center gap-2 mb-6">
          <div class="w-8 h-8 bg-mint-100 rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-800">检测趋势</h3>
        </div>

        <div v-if="trendData.length === 0" class="text-center py-16">
          <div class="w-16 h-16 bg-warmGray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-warmGray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
          <p class="text-gray-500">暂无趋势数据</p>
        </div>

        <div v-else class="space-y-8">
          <!-- 检出率趋势 -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-gray-600">震颤检出率 (%)</p>
              <div class="flex items-center gap-4 text-xs text-gray-400">
                <span class="flex items-center gap-1">
                  <span class="w-3 h-3 bg-primary-500 rounded"></span>
                  ≤50%
                </span>
                <span class="flex items-center gap-1">
                  <span class="w-3 h-3 bg-amber-500 rounded"></span>
                  >50%
                </span>
              </div>
            </div>
            <div class="bg-warmGray-50 rounded-xl p-4">
              <div class="h-40 flex items-end gap-1.5">
                <div
                  v-for="(point, index) in trendData"
                  :key="index"
                  class="flex-1 rounded-t-lg transition-all duration-500 group relative cursor-pointer hover:opacity-80"
                  :style="{
                    height: `${Math.max(4, (point.detection_rate / getMaxTrendValue()) * 100)}%`,
                    backgroundColor: point.detection_rate > 50 ? '#F59E0B' : '#F97316',
                    animationDelay: `${index * 30}ms`
                  }"
                >
                  <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none z-10 shadow-lg">
                    <div class="font-medium">{{ formatDate(point.date) }}</div>
                    <div class="text-primary-300">检出率: {{ point.detection_rate }}%</div>
                    <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                      <div class="border-4 border-transparent border-t-gray-800"></div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="flex justify-between text-xs text-gray-400 mt-2 px-1">
                <span>{{ formatDate(trendData[0]?.date) }}</span>
                <span>{{ formatDate(trendData[trendData.length - 1]?.date) }}</span>
              </div>
            </div>
          </div>

          <!-- 严重度趋势 -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <p class="text-sm font-medium text-gray-600">平均严重度</p>
              <div class="flex items-center gap-2 text-xs text-gray-400">
                <span>颜色表示严重程度</span>
              </div>
            </div>
            <div class="bg-warmGray-50 rounded-xl p-4">
              <div class="h-24 flex items-end gap-1.5">
                <div
                  v-for="(point, index) in trendData"
                  :key="index"
                  class="flex-1 rounded-t-lg transition-all duration-500 group relative cursor-pointer hover:opacity-80"
                  :style="{
                    height: point.avg_severity ? `${(point.avg_severity / 4) * 100}%` : '4%',
                    backgroundColor: point.avg_severity ? getSeverityColor(Math.round(point.avg_severity)) : '#E5E7EB',
                    animationDelay: `${index * 30}ms`
                  }"
                >
                  <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 whitespace-nowrap pointer-events-none z-10 shadow-lg">
                    <div class="font-medium">{{ formatDate(point.date) }}</div>
                    <div>平均严重度: {{ point.avg_severity?.toFixed(2) || '-' }}</div>
                    <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                      <div class="border-4 border-transparent border-t-gray-800"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 详细统计 -->
      <div class="card">
        <div class="flex items-center gap-2 mb-6">
          <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-800">详细统计</h3>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-5 bg-gradient-to-br from-warmGray-50 to-primary-50/30 rounded-2xl">
            <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <p class="text-gray-500 text-sm mb-1">平均频率</p>
            <p class="text-xl font-bold text-gray-800">
              {{ summary.avg_frequency ? `${summary.avg_frequency} Hz` : '-' }}
            </p>
          </div>

          <div class="text-center p-5 bg-gradient-to-br from-warmGray-50 to-amber-50/30 rounded-2xl">
            <div class="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <p class="text-gray-500 text-sm mb-1">平均振幅</p>
            <p class="text-xl font-bold text-gray-800">
              {{ summary.avg_amplitude ? `${summary.avg_amplitude} g` : '-' }}
            </p>
          </div>

          <div class="text-center p-5 bg-gradient-to-br from-warmGray-50 to-lavender-50/30 rounded-2xl">
            <div class="w-10 h-10 bg-lavender-100 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg class="w-5 h-5 text-lavender-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <p class="text-gray-500 text-sm mb-1">总会话数</p>
            <p class="text-xl font-bold text-gray-800">{{ summary.total_sessions }}</p>
          </div>

          <div class="text-center p-5 bg-gradient-to-br from-warmGray-50 to-mint-50/30 rounded-2xl">
            <div class="w-10 h-10 bg-mint-100 rounded-xl flex items-center justify-center mx-auto mb-3">
              <svg class="w-5 h-5 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <p class="text-gray-500 text-sm mb-1">最高严重度</p>
            <p class="text-xl font-bold">
              <span class="severity-badge" :class="`severity-${summary.max_severity}`">
                {{ getSeverityLabel(summary.max_severity) }}
              </span>
            </p>
          </div>
        </div>
      </div>
    </template>

    <!-- 无数据状态 -->
    <div v-else-if="!loading && !error" class="card text-center py-16">
      <div class="w-20 h-20 bg-gradient-to-br from-warmGray-100 to-warmGray-200 rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-warmGray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">暂无分析数据</h3>
      <p class="text-gray-500">开始监测后将显示统计分析</p>
      <RouterLink to="/monitor" class="btn btn-primary mt-6 inline-flex">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        开始监测
      </RouterLink>
    </div>
  </AppLayout>
</template>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.4s ease-out forwards;
  opacity: 0;
}
</style>
