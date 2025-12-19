<template>
  <div class="min-h-screen bg-gray-900 text-white p-6">
    <div class="max-w-7xl mx-auto">
      <!-- 页面标题 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-cyan-400">ESP32 数据测试</h1>
          <p class="text-gray-400 mt-1">实时接收和显示设备发送的数据包</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="refreshData"
            :disabled="loading"
            class="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 rounded-lg flex items-center gap-2 disabled:opacity-50"
          >
            <svg class="w-5 h-5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            刷新
          </button>
          <button
            @click="toggleAutoRefresh"
            :class="autoRefresh ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-600 hover:bg-gray-700'"
            class="px-4 py-2 rounded-lg flex items-center gap-2"
          >
            <span class="w-2 h-2 rounded-full" :class="autoRefresh ? 'bg-green-300 animate-pulse' : 'bg-gray-400'"></span>
            {{ autoRefresh ? '自动刷新中' : '自动刷新' }}
          </button>
          <button
            @click="clearPackets"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg"
          >
            清空数据
          </button>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="text-gray-400 text-sm">总数据包</div>
          <div class="text-2xl font-bold text-cyan-400">{{ stats.total_packets || 0 }}</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="text-gray-400 text-sm">最大容量</div>
          <div class="text-2xl font-bold text-yellow-400">{{ stats.max_packets || 500 }}</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="text-gray-400 text-sm">设备 IP</div>
          <div class="text-lg font-mono text-green-400">
            {{ (stats.recent_client_ips || []).join(', ') || '-' }}
          </div>
        </div>
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="text-gray-400 text-sm">最新数据时间</div>
          <div class="text-lg font-mono text-purple-400">
            {{ formatTime(stats.newest_packet) }}
          </div>
        </div>
      </div>

      <!-- API 端点说明 -->
      <div class="bg-gray-800 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-cyan-400 mb-3">ESP32 API 端点</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm font-mono">
          <div class="bg-gray-700 rounded p-3">
            <div class="text-green-400">POST</div>
            <div class="text-white">/api/test/receive</div>
            <div class="text-gray-400 text-xs mt-1">接收任意 JSON 数据</div>
          </div>
          <div class="bg-gray-700 rounded p-3">
            <div class="text-green-400">POST</div>
            <div class="text-white">/api/test/heartbeat</div>
            <div class="text-gray-400 text-xs mt-1">设备心跳</div>
          </div>
          <div class="bg-gray-700 rounded p-3">
            <div class="text-green-400">POST</div>
            <div class="text-white">/api/test/batch</div>
            <div class="text-gray-400 text-xs mt-1">批量数据上传</div>
          </div>
        </div>
      </div>

      <!-- 数据包列表 -->
      <div class="bg-gray-800 rounded-lg overflow-hidden">
        <div class="p-4 border-b border-gray-700 flex items-center justify-between">
          <h2 class="text-lg font-semibold">数据包列表</h2>
          <div class="text-sm text-gray-400">
            显示 {{ packets.length }} / {{ stats.total_packets || 0 }} 条
          </div>
        </div>

        <!-- 数据包表格 -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-700 text-left text-sm">
              <tr>
                <th class="p-3 w-16">ID</th>
                <th class="p-3 w-24">类型</th>
                <th class="p-3 w-32">来源 IP</th>
                <th class="p-3 w-40">时间</th>
                <th class="p-3">数据预览</th>
                <th class="p-3 w-20">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="packet in packets"
                :key="packet.id"
                class="border-t border-gray-700 hover:bg-gray-750"
              >
                <td class="p-3 font-mono text-cyan-400">#{{ packet.id }}</td>
                <td class="p-3">
                  <span
                    :class="getTypeClass(packet.type)"
                    class="px-2 py-1 rounded text-xs font-medium"
                  >
                    {{ packet.type || 'data' }}
                  </span>
                </td>
                <td class="p-3 font-mono text-sm">{{ packet.client_ip }}</td>
                <td class="p-3 font-mono text-sm text-gray-400">
                  {{ formatTime(packet.received_at) }}
                </td>
                <td class="p-3">
                  <pre class="text-xs text-gray-300 max-w-xl overflow-hidden text-ellipsis">{{ getDataPreview(packet.data) }}</pre>
                </td>
                <td class="p-3">
                  <button
                    @click="showDetail(packet)"
                    class="text-cyan-400 hover:text-cyan-300 text-sm"
                  >
                    详情
                  </button>
                </td>
              </tr>
              <tr v-if="packets.length === 0">
                <td colspan="6" class="p-8 text-center text-gray-500">
                  <div class="flex flex-col items-center">
                    <svg class="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                    </svg>
                    <p>暂无数据包</p>
                    <p class="text-sm mt-1">等待 ESP32 设备发送数据...</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 详情弹窗 -->
      <div
        v-if="selectedPacket"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click.self="selectedPacket = null"
      >
        <div class="bg-gray-800 rounded-lg max-w-4xl w-full max-h-[80vh] overflow-hidden">
          <div class="p-4 border-b border-gray-700 flex items-center justify-between">
            <h3 class="text-lg font-semibold">
              数据包详情 #{{ selectedPacket.id }}
            </h3>
            <button
              @click="selectedPacket = null"
              class="text-gray-400 hover:text-white"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="p-4 overflow-y-auto max-h-[calc(80vh-60px)]">
            <!-- 基本信息 -->
            <div class="grid grid-cols-2 gap-4 mb-4">
              <div class="bg-gray-700 rounded p-3">
                <div class="text-gray-400 text-sm">接收时间</div>
                <div class="font-mono">{{ selectedPacket.received_at }}</div>
              </div>
              <div class="bg-gray-700 rounded p-3">
                <div class="text-gray-400 text-sm">客户端 IP</div>
                <div class="font-mono">{{ selectedPacket.client_ip }}</div>
              </div>
            </div>

            <!-- Headers -->
            <div class="mb-4">
              <h4 class="text-sm text-gray-400 mb-2">HTTP Headers</h4>
              <pre class="bg-gray-900 rounded p-3 text-xs overflow-x-auto">{{ JSON.stringify(selectedPacket.headers, null, 2) }}</pre>
            </div>

            <!-- Data -->
            <div>
              <h4 class="text-sm text-gray-400 mb-2">数据内容</h4>
              <pre class="bg-gray-900 rounded p-3 text-sm overflow-x-auto text-green-400">{{ JSON.stringify(selectedPacket.data, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

interface Packet {
  id: number
  received_at: string
  type?: string
  client_ip: string
  headers?: Record<string, string>
  data: unknown
}

interface Stats {
  total_packets: number
  max_packets: number
  type_counts: Record<string, number>
  recent_client_ips: string[]
  oldest_packet: string | null
  newest_packet: string | null
}

const packets = ref<Packet[]>([])
const stats = ref<Partial<Stats>>({})
const loading = ref(false)
const autoRefresh = ref(false)
const selectedPacket = ref<Packet | null>(null)

let refreshInterval: number | null = null

const apiBase = import.meta.env.VITE_API_BASE_URL || '/api'

async function fetchStats() {
  try {
    const response = await axios.get(`${apiBase}/test/stats`)
    stats.value = response.data
  } catch (error) {
    console.error('获取统计失败:', error)
  }
}

async function fetchPackets() {
  try {
    const response = await axios.get(`${apiBase}/test/packets`, {
      params: { limit: 50 }
    })
    packets.value = response.data.packets
  } catch (error) {
    console.error('获取数据包失败:', error)
  }
}

async function refreshData() {
  loading.value = true
  try {
    await Promise.all([fetchStats(), fetchPackets()])
  } finally {
    loading.value = false
  }
}

async function clearPackets() {
  if (!confirm('确定要清空所有数据包吗？')) return

  try {
    await axios.delete(`${apiBase}/test/packets`)
    await refreshData()
  } catch (error) {
    console.error('清空失败:', error)
  }
}

function toggleAutoRefresh() {
  autoRefresh.value = !autoRefresh.value

  if (autoRefresh.value) {
    refreshInterval = window.setInterval(refreshData, 2000)
  } else if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

function showDetail(packet: Packet) {
  selectedPacket.value = packet
}

function formatTime(isoString: string | null | undefined): string {
  if (!isoString) return '-'
  try {
    const date = new Date(isoString)
    return date.toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch {
    return isoString
  }
}

function getDataPreview(data: unknown): string {
  const str = JSON.stringify(data)
  if (str.length > 100) {
    return str.substring(0, 100) + '...'
  }
  return str
}

function getTypeClass(type: string | undefined): string {
  switch (type) {
    case 'heartbeat':
      return 'bg-green-600 text-green-100'
    case 'batch':
      return 'bg-purple-600 text-purple-100'
    default:
      return 'bg-cyan-600 text-cyan-100'
  }
}

onMounted(() => {
  refreshData()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.bg-gray-750 {
  background-color: rgb(55, 65, 81);
}
</style>
