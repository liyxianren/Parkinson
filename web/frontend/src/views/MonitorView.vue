<script setup lang="ts">
import { ref } from 'vue'

const isMonitoring = ref(false)

function toggleMonitoring() {
  isMonitoring.value = !isMonitoring.value
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <h1 class="text-2xl font-bold mb-6">实时监测</h1>

    <div class="card text-center py-12">
      <div
        class="w-32 h-32 rounded-full mx-auto mb-6 flex items-center justify-center transition-colors"
        :class="isMonitoring ? 'bg-green-100' : 'bg-gray-100'"
      >
        <svg
          class="w-16 h-16 transition-colors"
          :class="isMonitoring ? 'text-green-600' : 'text-gray-400'"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>

      <h2 class="text-xl font-semibold mb-2">
        {{ isMonitoring ? '监测中...' : '准备就绪' }}
      </h2>
      <p class="text-gray-500 mb-6">
        {{ isMonitoring ? '正在接收设备数据' : '点击下方按钮开始监测' }}
      </p>

      <button
        @click="toggleMonitoring"
        class="btn text-lg px-8 py-3"
        :class="isMonitoring ? 'btn-danger' : 'btn-primary'"
      >
        {{ isMonitoring ? '停止监测' : '开始监测' }}
      </button>

      <p class="text-sm text-gray-400 mt-8">
        提示: 请确保设备已连接并处于在线状态
      </p>
    </div>
  </div>
</template>
