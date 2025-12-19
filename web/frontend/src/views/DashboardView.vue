<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTremorStore } from '@/stores/tremor'
import { getSeverityLabel, getSeverityColor } from '@/types'

const tremorStore = useTremorStore()

// Mock data for demonstration
const stats = ref({
  todayAnalyses: 12,
  todayTremors: 8,
  avgSeverity: 1.8,
  maxSeverity: 3,
})

const recentSessions = ref([
  { id: 1, start: '10:30', duration: '15分钟', tremors: 5, maxSeverity: 2 },
  { id: 2, start: '14:00', duration: '20分钟', tremors: 3, maxSeverity: 1 },
])

onMounted(() => {
  tremorStore.fetchDailyStats()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar would go here -->

    <!-- Main Content -->
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-6">仪表盘</h1>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Today's Analyses -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">今日检测</p>
              <p class="text-3xl font-bold">{{ stats.todayAnalyses }}</p>
            </div>
            <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Tremor Count -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">震颤次数</p>
              <p class="text-3xl font-bold">{{ stats.todayTremors }}</p>
            </div>
            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Average Severity -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">平均严重度</p>
              <p class="text-3xl font-bold">{{ stats.avgSeverity.toFixed(1) }}</p>
            </div>
            <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Max Severity -->
        <div class="card">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-500 text-sm">最高严重度</p>
              <p class="text-3xl font-bold">
                <span
                  class="severity-badge"
                  :class="`severity-${stats.maxSeverity}`"
                >
                  {{ getSeverityLabel(stats.maxSeverity) }}
                </span>
              </p>
            </div>
            <div
              class="w-12 h-12 rounded-full flex items-center justify-center"
              :style="{ backgroundColor: getSeverityColor(stats.maxSeverity) + '20' }"
            >
              <span
                class="text-lg font-bold"
                :style="{ color: getSeverityColor(stats.maxSeverity) }"
              >
                {{ stats.maxSeverity }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Sessions -->
      <div class="card">
        <h2 class="text-xl font-semibold mb-4">今日检测记录</h2>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b">
                <th class="text-left py-3 px-4 text-gray-500 font-medium">时间</th>
                <th class="text-left py-3 px-4 text-gray-500 font-medium">时长</th>
                <th class="text-left py-3 px-4 text-gray-500 font-medium">震颤次数</th>
                <th class="text-left py-3 px-4 text-gray-500 font-medium">最高严重度</th>
                <th class="text-left py-3 px-4 text-gray-500 font-medium">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="session in recentSessions" :key="session.id" class="border-b hover:bg-gray-50">
                <td class="py-3 px-4">{{ session.start }}</td>
                <td class="py-3 px-4">{{ session.duration }}</td>
                <td class="py-3 px-4">{{ session.tremors }}</td>
                <td class="py-3 px-4">
                  <span class="severity-badge" :class="`severity-${session.maxSeverity}`">
                    {{ getSeverityLabel(session.maxSeverity) }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <button class="text-primary-600 hover:text-primary-700">查看详情</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <RouterLink to="/monitor" class="card hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="font-semibold">开始监测</h3>
            <p class="text-gray-500 text-sm">实时震颤检测</p>
          </div>
        </RouterLink>

        <RouterLink to="/ai-assistant" class="card hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="font-semibold">AI 助手</h3>
            <p class="text-gray-500 text-sm">智能健康建议</p>
          </div>
        </RouterLink>

        <RouterLink to="/reports" class="card hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="font-semibold">生成报告</h3>
            <p class="text-gray-500 text-sm">导出健康报告</p>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
