<template>
  <div class="min-h-screen bg-gray-900 text-white p-6">
    <div class="max-w-5xl mx-auto">
      <!-- 页面标题 -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-cyan-400">参数配置</h1>
          <p class="text-gray-400 mt-1">调整震颤检测算法的关键参数 (上位机模式)</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="refreshStatus"
            :disabled="loading"
            class="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg flex items-center gap-2"
          >
            <svg class="w-5 h-5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            刷新
          </button>
          <button
            @click="resetToDefaults"
            class="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg"
          >
            恢复默认
          </button>
          <button
            @click="saveConfig"
            :disabled="saving"
            class="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 rounded-lg flex items-center gap-2 disabled:opacity-50"
          >
            <svg v-if="!saving" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            保存配置
          </button>
        </div>
      </div>

      <!-- 状态卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- 设备状态 -->
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-lg font-semibold text-cyan-400">设备状态</h2>
            <span
              :class="deviceStatus.connected ? 'bg-green-600' : 'bg-gray-600'"
              class="px-2 py-1 rounded text-xs"
            >
              {{ deviceStatus.connected ? '已连接' : '未连接' }}
            </span>
          </div>
          <div v-if="deviceStatus.connected" class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-400">设备 ID:</span>
              <span class="font-mono text-green-400">{{ deviceStatus.device_id }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">设备 IP:</span>
              <span class="font-mono">{{ deviceStatus.ip }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">配置版本:</span>
              <span class="font-mono">v{{ deviceStatus.version }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">最后上报:</span>
              <span class="font-mono">{{ formatTime(deviceStatus.last_seen) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">同步状态:</span>
              <span :class="deviceStatus.synced ? 'text-green-400' : 'text-yellow-400'">
                {{ deviceStatus.synced ? '已同步' : '待同步' }}
              </span>
            </div>
          </div>
          <div v-else class="text-gray-500 text-sm">
            <p>等待设备连接...</p>
            <p class="mt-2 text-xs">设备需执行 <code class="bg-gray-700 px-1 rounded">cfgup</code> 命令上传配置</p>
          </div>
        </div>

        <!-- 云端配置状态 -->
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-lg font-semibold text-yellow-400">云端配置</h2>
            <span class="bg-blue-600 px-2 py-1 rounded text-xs">
              v{{ cloudStatus.version }}
            </span>
          </div>
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-400">配置来源:</span>
              <span class="font-mono">{{ getSourceLabel(cloudStatus.source) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">更新时间:</span>
              <span class="font-mono">{{ formatTime(cloudStatus.updated_at) }}</span>
            </div>
          </div>
          <div class="mt-4 p-3 bg-gray-700 rounded text-xs">
            <p class="text-gray-400 mb-2">使用流程:</p>
            <ol class="list-decimal list-inside space-y-1 text-gray-300">
              <li>设备执行 <code class="bg-gray-600 px-1 rounded">cfgup</code> 上传当前配置</li>
              <li>在此页面修改参数并保存</li>
              <li>设备执行 <code class="bg-gray-600 px-1 rounded">update</code> 拉取新配置</li>
            </ol>
          </div>
        </div>
      </div>

      <!-- 配置对比 (如果设备已连接) -->
      <div v-if="deviceStatus.connected && deviceStatus.params" class="bg-gray-800 rounded-lg p-4 mb-6">
        <h2 class="text-lg font-semibold text-purple-400 mb-3">配置对比</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-700 text-left">
              <tr>
                <th class="p-2">参数</th>
                <th class="p-2 text-green-400">设备当前值</th>
                <th class="p-2 text-yellow-400">云端配置值</th>
                <th class="p-2">状态</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-t border-gray-700">
                <td class="p-2">RMS 下限</td>
                <td class="p-2 font-mono">{{ deviceStatus.params.rms_min?.toFixed(2) }} g</td>
                <td class="p-2 font-mono">{{ config.rms_min.toFixed(2) }} g</td>
                <td class="p-2">
                  <span v-if="deviceStatus.params.rms_min === config.rms_min" class="text-green-400">✓</span>
                  <span v-else class="text-yellow-400">≠</span>
                </td>
              </tr>
              <tr class="border-t border-gray-700">
                <td class="p-2">RMS 上限</td>
                <td class="p-2 font-mono">{{ deviceStatus.params.rms_max?.toFixed(2) }} g</td>
                <td class="p-2 font-mono">{{ config.rms_max.toFixed(2) }} g</td>
                <td class="p-2">
                  <span v-if="deviceStatus.params.rms_max === config.rms_max" class="text-green-400">✓</span>
                  <span v-else class="text-yellow-400">≠</span>
                </td>
              </tr>
              <tr class="border-t border-gray-700">
                <td class="p-2">功率阈值</td>
                <td class="p-2 font-mono">{{ deviceStatus.params.power_threshold?.toFixed(2) }}</td>
                <td class="p-2 font-mono">{{ config.power_threshold.toFixed(2) }}</td>
                <td class="p-2">
                  <span v-if="deviceStatus.params.power_threshold === config.power_threshold" class="text-green-400">✓</span>
                  <span v-else class="text-yellow-400">≠</span>
                </td>
              </tr>
              <tr class="border-t border-gray-700">
                <td class="p-2">频率范围</td>
                <td class="p-2 font-mono">{{ deviceStatus.params.freq_min?.toFixed(1) }} - {{ deviceStatus.params.freq_max?.toFixed(1) }} Hz</td>
                <td class="p-2 font-mono">{{ config.freq_min.toFixed(1) }} - {{ config.freq_max.toFixed(1) }} Hz</td>
                <td class="p-2">
                  <span v-if="deviceStatus.params.freq_min === config.freq_min && deviceStatus.params.freq_max === config.freq_max" class="text-green-400">✓</span>
                  <span v-else class="text-yellow-400">≠</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 配置面板 -->
      <div class="space-y-6">
        <!-- RMS 幅度范围 -->
        <div class="bg-gray-800 rounded-lg p-6">
          <h2 class="text-lg font-semibold text-cyan-400 mb-4 flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            RMS 幅度范围 (g)
          </h2>
          <p class="text-gray-400 text-sm mb-4">
            定义有效震颤的 RMS 加速度范围。低于下限不判定为震颤，高于上限判定为超出范围。
          </p>

          <div class="space-y-4">
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm text-gray-300">下限 (rms_min)</label>
                <span class="font-mono text-cyan-400 text-lg">{{ config.rms_min.toFixed(1) }} g</span>
              </div>
              <input
                type="range"
                v-model.number="config.rms_min"
                min="0.1"
                max="5.0"
                step="0.1"
                class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
              />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>0.1</span>
                <span>5.0</span>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm text-gray-300">上限 (rms_max)</label>
                <span class="font-mono text-cyan-400 text-lg">{{ config.rms_max.toFixed(1) }} g</span>
              </div>
              <input
                type="range"
                v-model.number="config.rms_max"
                min="1.0"
                max="20.0"
                step="0.5"
                class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
              />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>1.0</span>
                <span>20.0</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 功率阈值 -->
        <div class="bg-gray-800 rounded-lg p-6">
          <h2 class="text-lg font-semibold text-yellow-400 mb-4 flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            功率阈值
          </h2>
          <p class="text-gray-400 text-sm mb-4">
            震颤频段 (4-6Hz) 的功率需超过此阈值才判定为震颤。降低此值可提高灵敏度。
          </p>

          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-sm text-gray-300">power_threshold</label>
              <span class="font-mono text-yellow-400 text-lg">{{ config.power_threshold.toFixed(2) }}</span>
            </div>
            <input
              type="range"
              v-model.number="config.power_threshold"
              min="0.01"
              max="2.0"
              step="0.01"
              class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-yellow"
            />
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>0.01 (高灵敏度)</span>
              <span>2.0 (低灵敏度)</span>
            </div>
          </div>
        </div>

        <!-- 频率范围 -->
        <div class="bg-gray-800 rounded-lg p-6">
          <h2 class="text-lg font-semibold text-green-400 mb-4 flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
            频率范围 (Hz)
          </h2>
          <p class="text-gray-400 text-sm mb-4">
            帕金森震颤的典型频率为 4-6Hz。调整此范围可适应不同类型的震颤检测。
          </p>

          <div class="space-y-4">
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm text-gray-300">下限 (freq_min)</label>
                <span class="font-mono text-green-400 text-lg">{{ config.freq_min.toFixed(1) }} Hz</span>
              </div>
              <input
                type="range"
                v-model.number="config.freq_min"
                min="1.0"
                max="8.0"
                step="0.5"
                class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-green"
              />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>1.0</span>
                <span>8.0</span>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm text-gray-300">上限 (freq_max)</label>
                <span class="font-mono text-green-400 text-lg">{{ config.freq_max.toFixed(1) }} Hz</span>
              </div>
              <input
                type="range"
                v-model.number="config.freq_max"
                min="4.0"
                max="15.0"
                step="0.5"
                class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-green"
              />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>4.0</span>
                <span>15.0</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 严重度分级阈值 -->
        <div class="bg-gray-800 rounded-lg p-6">
          <h2 class="text-lg font-semibold text-purple-400 mb-4 flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            严重度分级阈值 (g)
          </h2>
          <p class="text-gray-400 text-sm mb-4">
            根据 RMS 幅度将震颤分为 0-4 级。数值为各级别的分界点。
          </p>

          <div class="space-y-4">
            <div v-for="(label, index) in severityLabels" :key="index">
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm text-gray-300">
                  <span :class="getSeverityColor(index)" class="px-2 py-0.5 rounded text-xs mr-2">{{ index }}级</span>
                  {{ label }}
                </label>
                <span class="font-mono text-purple-400 text-lg">{{ config.severity_thresholds[index]?.toFixed(1) }} g</span>
              </div>
              <input
                type="range"
                v-model.number="config.severity_thresholds[index]"
                min="0.5"
                max="8.0"
                step="0.1"
                class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider-purple"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 保存成功提示 -->
      <div
        v-if="saveSuccess"
        class="fixed bottom-6 right-6 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        配置已保存 (版本 v{{ cloudStatus.version }})
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

interface TremorConfig {
  rms_min: number
  rms_max: number
  power_threshold: number
  freq_min: number
  freq_max: number
  severity_thresholds: number[]
}

interface DeviceStatus {
  connected: boolean
  version: number
  last_seen: string | null
  ip: string | null
  device_id: string | null
  params: TremorConfig | null
  synced: boolean
}

interface CloudStatus {
  version: number
  updated_at: string
  source: string
  params: TremorConfig
}

const config = reactive<TremorConfig>({
  rms_min: 2.5,
  rms_max: 5.0,
  power_threshold: 0.5,
  freq_min: 4.0,
  freq_max: 6.0,
  severity_thresholds: [2.5, 3.0, 3.5, 4.0]
})

const deviceStatus = reactive<DeviceStatus>({
  connected: false,
  version: 0,
  last_seen: null,
  ip: null,
  device_id: null,
  params: null,
  synced: false
})

const cloudStatus = reactive<CloudStatus>({
  version: 1,
  updated_at: '',
  source: 'default',
  params: { ...config }
})

const loading = ref(false)
const saving = ref(false)
const saveSuccess = ref(false)

const severityLabels = ['无/极轻', '轻微', '轻度', '中度']

const apiBase = import.meta.env.VITE_API_BASE_URL || '/api'

let refreshInterval: number | null = null

async function loadStatus() {
  try {
    const response = await axios.get(`${apiBase}/config/status`)
    const data = response.data

    // 更新云端状态
    cloudStatus.version = data.cloud.version
    cloudStatus.updated_at = data.cloud.updated_at
    cloudStatus.source = data.cloud.source
    Object.assign(config, data.cloud.params)

    // 更新设备状态
    deviceStatus.connected = data.device.connected
    deviceStatus.version = data.device.version
    deviceStatus.last_seen = data.device.last_seen
    deviceStatus.ip = data.device.ip
    deviceStatus.device_id = data.device.device_id
    deviceStatus.params = data.device.params
    deviceStatus.synced = data.device.synced
  } catch (error) {
    console.error('加载状态失败:', error)
  }
}

async function refreshStatus() {
  loading.value = true
  try {
    await loadStatus()
  } finally {
    loading.value = false
  }
}

async function saveConfig() {
  saving.value = true
  try {
    const response = await axios.post(`${apiBase}/config/save`, {
      rms_min: config.rms_min,
      rms_max: config.rms_max,
      power_threshold: config.power_threshold,
      freq_min: config.freq_min,
      freq_max: config.freq_max,
      severity_thresholds: config.severity_thresholds
    })

    cloudStatus.version = response.data.version
    cloudStatus.updated_at = response.data.updated_at
    cloudStatus.source = 'web'

    // 更新同步状态
    deviceStatus.synced = deviceStatus.version >= cloudStatus.version

    // 显示成功提示
    saveSuccess.value = true
    setTimeout(() => {
      saveSuccess.value = false
    }, 3000)
  } catch (error) {
    console.error('保存配置失败:', error)
    alert('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

async function resetToDefaults() {
  if (!confirm('确定要恢复默认配置吗？')) return

  try {
    const response = await axios.post(`${apiBase}/config/reset`)
    cloudStatus.version = response.data.version
    cloudStatus.updated_at = response.data.updated_at

    // 重新加载状态
    await loadStatus()
  } catch (error) {
    console.error('重置配置失败:', error)
  }
}

function formatTime(isoString: string | null | undefined): string {
  if (!isoString) return '-'
  try {
    const date = new Date(isoString)
    return date.toLocaleString('zh-CN')
  } catch {
    return isoString
  }
}

function getSourceLabel(source: string): string {
  switch (source) {
    case 'default': return '默认配置'
    case 'device': return '设备上传'
    case 'web': return '网页修改'
    default: return source
  }
}

function getSeverityColor(level: number): string {
  const colors = [
    'bg-gray-600',
    'bg-yellow-600',
    'bg-orange-600',
    'bg-red-600'
  ]
  return colors[level] || 'bg-gray-600'
}

onMounted(() => {
  loadStatus()
  // 每 5 秒刷新一次状态
  refreshInterval = window.setInterval(loadStatus, 5000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
/* 自定义滑块样式 */
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #22d3ee;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #22d3ee;
  cursor: pointer;
  border: none;
}

.slider-yellow::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #facc15;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(250, 204, 21, 0.5);
}

.slider-yellow::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #facc15;
  cursor: pointer;
  border: none;
}

.slider-green::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4ade80;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
}

.slider-green::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4ade80;
  cursor: pointer;
  border: none;
}

.slider-purple::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #c084fc;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(192, 132, 252, 0.5);
}

.slider-purple::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #c084fc;
  cursor: pointer;
  border: none;
}
</style>
