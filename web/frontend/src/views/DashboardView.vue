<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useTremorStore } from '@/stores/tremor'
import { useAuthStore } from '@/stores/auth'
import { getSeverityLabel, getSeverityColor } from '@/types'
import AppLayout from '@/layouts/AppLayout.vue'

const tremorStore = useTremorStore()
const authStore = useAuthStore()

const loading = ref(true)

// 计算属性
const stats = computed(() => {
  if (tremorStore.todayStats) {
    return {
      todayAnalyses: tremorStore.todayStats.total_analyses,
      todayTremors: tremorStore.todayStats.tremor_detections,
      avgSeverity: tremorStore.todayStats.avg_severity,
      maxSeverity: tremorStore.todayStats.max_severity,
      detectionRate: tremorStore.todayStats.detection_rate,
      totalSessions: tremorStore.todayStats.total_sessions,
    }
  }
  return {
    todayAnalyses: 0,
    todayTremors: 0,
    avgSeverity: 0,
    maxSeverity: 0,
    detectionRate: 0,
    totalSessions: 0,
  }
})

const recentSessions = computed(() => {
  return tremorStore.sessions.slice(0, 5).map(session => ({
    id: session.id,
    start: new Date(session.start_time).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    duration: session.duration_seconds
      ? `${Math.floor(session.duration_seconds / 60)}分钟`
      : '进行中',
    tremors: session.tremor_count,
    maxSeverity: session.max_severity,
    isActive: session.is_active,
  }))
})

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      tremorStore.fetchTodayStats(),
      tremorStore.fetchSessions(10)
    ])
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-64">
        <div class="text-center">
          <div class="relative w-16 h-16 mx-auto mb-4">
            <div class="absolute inset-0 rounded-full border-4 border-primary-100"></div>
            <div class="absolute inset-0 rounded-full border-4 border-primary-500 border-t-transparent animate-spin"></div>
          </div>
          <p class="text-gray-500">加载数据中...</p>
        </div>
      </div>

      <template v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <!-- Today's Analyses -->
          <div class="card-gradient group">
            <div class="flex items-start justify-between">
              <div>
                <p class="text-gray-500 text-sm font-medium">今日检测</p>
                <p class="text-4xl font-bold text-gray-800 mt-2">{{ stats.todayAnalyses }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <span class="badge badge-primary">
                    {{ stats.totalSessions }} 次会话
                  </span>
                </div>
              </div>
              <div class="w-14 h-14 bg-gradient-to-br from-primary-400 to-primary-500 rounded-2xl flex items-center justify-center shadow-soft group-hover:shadow-glow transition-shadow">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Tremor Count -->
          <div class="card-gradient group">
            <div class="flex items-start justify-between">
              <div>
                <p class="text-gray-500 text-sm font-medium">震颤次数</p>
                <p class="text-4xl font-bold text-gray-800 mt-2">{{ stats.todayTremors }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <span class="badge badge-warning">
                    检出率 {{ stats.detectionRate }}%
                  </span>
                </div>
              </div>
              <div class="w-14 h-14 bg-gradient-to-br from-yellow-400 to-orange-400 rounded-2xl flex items-center justify-center shadow-soft group-hover:shadow-glow transition-shadow">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Average Severity -->
          <div class="card-gradient group">
            <div class="flex items-start justify-between">
              <div>
                <p class="text-gray-500 text-sm font-medium">平均严重度</p>
                <p class="text-4xl font-bold text-gray-800 mt-2">{{ stats.avgSeverity.toFixed(1) }}</p>
                <div class="mt-3">
                  <div class="progress !h-2.5 !bg-warmGray-200">
                    <div
                      class="progress-bar"
                      :style="{ width: `${(stats.avgSeverity / 4) * 100}%` }"
                    ></div>
                  </div>
                </div>
              </div>
              <div class="w-14 h-14 bg-gradient-to-br from-orange-400 to-red-400 rounded-2xl flex items-center justify-center shadow-soft group-hover:shadow-glow transition-shadow">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          <!-- Max Severity -->
          <div class="card-gradient group">
            <div class="flex items-start justify-between">
              <div>
                <p class="text-gray-500 text-sm font-medium">最高严重度</p>
                <div class="mt-3">
                  <span
                    class="severity-badge text-lg"
                    :class="`severity-${stats.maxSeverity}`"
                  >
                    {{ getSeverityLabel(stats.maxSeverity) }}
                  </span>
                </div>
              </div>
              <div
                class="w-14 h-14 rounded-2xl flex items-center justify-center shadow-soft"
                :style="{
                  background: `linear-gradient(135deg, ${getSeverityColor(stats.maxSeverity)}80, ${getSeverityColor(stats.maxSeverity)})`
                }"
              >
                <span class="text-2xl font-bold text-white">
                  {{ stats.maxSeverity }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Sessions -->
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-xl font-bold text-gray-800">最近检测记录</h2>
              <p class="text-sm text-gray-500 mt-1">您最近的震颤监测会话</p>
            </div>
            <RouterLink to="/history" class="btn btn-ghost btn-sm">
              查看全部
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </RouterLink>
          </div>

          <div v-if="recentSessions.length === 0" class="empty-state">
            <div class="w-20 h-20 bg-warmGray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-10 h-10 text-warmGray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-600 mb-2">暂无检测记录</h3>
            <p class="text-gray-400 mb-6">开始您的第一次震颤监测吧</p>
            <RouterLink to="/monitor" class="btn btn-primary">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              开始监测
            </RouterLink>
          </div>

          <div v-else class="table-container !shadow-none !rounded-none">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>时间</th>
                  <th>时长</th>
                  <th>震颤次数</th>
                  <th>最高严重度</th>
                  <th>状态</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(session, index) in recentSessions"
                  :key="session.id"
                  class="animate-fade-in-up"
                  :style="{ animationDelay: `${index * 50}ms` }"
                >
                  <td class="font-medium">{{ session.start }}</td>
                  <td>{{ session.duration }}</td>
                  <td>
                    <span class="font-semibold">{{ session.tremors }}</span>
                  </td>
                  <td>
                    <span class="severity-badge" :class="`severity-${session.maxSeverity}`">
                      {{ getSeverityLabel(session.maxSeverity) }}
                    </span>
                  </td>
                  <td>
                    <span
                      :class="[
                        'badge',
                        session.isActive ? 'badge-success' : 'bg-warmGray-100 text-gray-600'
                      ]"
                    >
                      <span v-if="session.isActive" class="w-2 h-2 bg-mint-500 rounded-full animate-pulse mr-1.5"></span>
                      {{ session.isActive ? '进行中' : '已完成' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <RouterLink
            to="/monitor"
            class="card-gradient group cursor-pointer !p-8 text-center hover:shadow-glow transition-all duration-300"
          >
            <div class="w-20 h-20 bg-gradient-to-br from-mint-400 to-mint-500 rounded-3xl flex items-center justify-center mx-auto mb-5 shadow-soft group-hover:scale-105 transition-transform">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">开始监测</h3>
            <p class="text-gray-500">实时震颤检测与分析</p>
          </RouterLink>

          <RouterLink
            to="/ai-assistant"
            class="card-gradient group cursor-pointer !p-8 text-center hover:shadow-glow transition-all duration-300"
          >
            <div class="w-20 h-20 bg-gradient-to-br from-lavender-400 to-lavender-500 rounded-3xl flex items-center justify-center mx-auto mb-5 shadow-soft group-hover:scale-105 transition-transform">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">AI 助手</h3>
            <p class="text-gray-500">获取智能健康建议</p>
          </RouterLink>

          <RouterLink
            to="/reports"
            class="card-gradient group cursor-pointer !p-8 text-center hover:shadow-glow transition-all duration-300"
          >
            <div class="w-20 h-20 bg-gradient-to-br from-primary-400 to-primary-500 rounded-3xl flex items-center justify-center mx-auto mb-5 shadow-soft group-hover:scale-105 transition-transform">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">生成报告</h3>
            <p class="text-gray-500">导出专业健康报告</p>
          </RouterLink>
        </div>

        <!-- Tips Section -->
        <div class="card-gradient !p-6 relative overflow-hidden">
          <div class="absolute -top-8 -right-8 w-24 h-24 bg-primary-200/50 rounded-full"></div>
          <div class="absolute -bottom-4 -left-4 w-16 h-16 bg-primary-100/50 rounded-full"></div>

          <div class="relative flex items-start gap-4">
            <div class="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800 mb-1">健康小贴士</h3>
              <p class="text-gray-600 text-sm leading-relaxed">
                规律的运动和充足的睡眠有助于减轻帕金森症状。建议每天保持适度的体育活动，
                如散步、太极或瑜伽。同时，保持乐观的心态也很重要。
              </p>
            </div>
          </div>
        </div>
      </template>
    </div>
  </AppLayout>
</template>
