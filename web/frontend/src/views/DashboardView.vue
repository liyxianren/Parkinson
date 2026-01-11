<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import TrendChart from '@/components/charts/TrendChart.vue'
import { mockService } from '@/services/mock'
import { getSeverityLabel, getSeverityColor } from '@/types'

const loading = ref(true)

// Mock Data
const stats = ref({
    todayAnalyses: 12,
    todayTremors: 45,
    avgSeverity: 1.8,
    maxSeverity: 3,
    detectionRate: 25,
    totalSessions: 4
})

const trendData = ref<{ labels: string[], severity: number[], counts: number[] }>({
    labels: [], severity: [], counts: []
})

const recentSessions = ref<any[]>([])

onMounted(async () => {
  loading.value = true
  
  // Simulate API delay
  setTimeout(() => {
      // Load Trend Data
      const history = mockService.generateTrendData(7)
      trendData.value.labels = history.map(d => {
          const date = new Date(d.date)
          return `${date.getMonth()+1}-${date.getDate()}`
      })
      trendData.value.severity = history.map(d => d.avg_severity)
      trendData.value.counts = history.map(d => d.tremor_count)
      
      // Load Recent Sessions
      recentSessions.value = [
          { id: 1, start: '14:30', duration: '15分钟', tremors: 12, maxSeverity: 2, isActive: false },
          { id: 2, start: '10:15', duration: '20分钟', tremors: 5, maxSeverity: 1, isActive: false },
          { id: 3, start: '08:45', duration: '10分钟', tremors: 28, maxSeverity: 3, isActive: false },
      ]
      
      loading.value = false
  }, 600)
})

</script>

<template>
  <AppLayout>
    <div class="space-y-6">
      
      <!-- Welcome Header -->
      <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-800">下午好，李先生</h1>
            <p class="text-gray-500 mt-1">这里是您的今日震颤监测概览</p>
          </div>
          <div class="text-right hidden md:block">
              <p class="text-sm text-gray-500">上次同步</p>
              <p class="font-medium text-gray-700">刚刚</p>
          </div>
      </div>

      <div v-if="loading" class="flex items-center justify-center h-64">
        <!-- Keep loading state simple -->
        <div class="text-center text-gray-500">加载中...</div>
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

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Left: Trend Chart -->
            <div class="lg:col-span-2">
                <div class="card h-full">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="font-bold text-gray-800 text-lg">本周震颤趋势</h3>
                        <select class="px-3 py-1 bg-warmGray-50 border border-warmGray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-100">
                            <option>近7天</option>
                            <option>近30天</option>
                        </select>
                    </div>
                    <TrendChart 
                        :date-labels="trendData.labels" 
                        :severity-data="trendData.severity"
                        :tremor-count-data="trendData.counts"
                    />
                </div>
            </div>

            <!-- Right: Activity & Tips -->
            <div class="space-y-6">
                 <!-- Recent Sessions List -->
                 <div class="card">
                     <div class="flex items-center justify-between mb-4">
                         <h3 class="font-bold text-gray-800">最近记录</h3>
                         <RouterLink to="/history" class="text-sm text-primary-600 hover:text-primary-700 font-medium">查看全部</RouterLink>
                     </div>
                     <div class="space-y-3">
                         <div v-for="session in recentSessions" :key="session.id" class="flex items-center justify-between p-3 bg-warmGray-50 rounded-xl hover:bg-white hover:shadow-sm transition-all cursor-pointer border border-transparent hover:border-warmGray-100">
                             <div class="flex items-center gap-3">
                                 <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center text-gray-500 shadow-sm text-xs font-bold">
                                     {{ session.start }}
                                 </div>
                                 <div>
                                     <p class="text-sm font-bold text-gray-800">{{ session.duration }}</p>
                                     <p class="text-xs text-gray-500">{{ session.tremors }}次震颤</p>
                                 </div>
                             </div>
                             <span class="severity-badge scale-90" :class="`severity-${session.maxSeverity}`">
                                {{ getSeverityLabel(session.maxSeverity) }}
                             </span>
                         </div>
                     </div>
                 </div>

                 <!-- AI Assistant Card -->
                 <div class="card-gradient !from-lavender-50 !to-lavender-100/50 border border-lavender-100 relative overflow-hidden">
                      <div class="relative z-10">
                          <h3 class="font-bold text-gray-800 mb-2">AI 健康助手</h3>
                          <p class="text-sm text-gray-600 mb-4">基于您的一周数据，AI 分析建议您适当增加上午的康复训练时长。</p>
                          <RouterLink to="/ai-assistant" class="btn btn-lavender btn-sm w-full">咨询 AI 助手</RouterLink>
                      </div>
                      <div class="absolute -bottom-4 -right-4 w-24 h-24 bg-lavender-200/50 rounded-full blur-xl"></div>
                 </div>
            </div>
        </div>

      </template>
    </div>
  </AppLayout>
</template>
