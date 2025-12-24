<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { aiApi, type ChatMessage, type AnalysisResponse, type InsightsResponse } from '@/api/ai'

// 聊天相关
const messages = ref<ChatMessage[]>([])
const inputMessage = ref('')
const isLoading = ref(false)
const chatContainer = ref<HTMLElement | null>(null)

// 分析相关
const analysisResult = ref<AnalysisResponse | null>(null)
const isAnalyzing = ref(false)
const analysisDays = ref(7)

// 洞察和提示
const insights = ref<InsightsResponse | null>(null)
const healthTips = ref<string[]>([])
const loadingInsights = ref(false)

// 当前标签页
const activeTab = ref<'chat' | 'analysis' | 'insights'>('chat')

// 快捷问题
const quickQuestions = [
  '我的震颤数据说明什么？',
  '帕金森病震颤有什么特点？',
  '如何减轻震颤症状？',
  '什么时候应该去看医生？',
  '有哪些日常护理建议？'
]

// 计算属性
const conversationHistory = computed(() => {
  return messages.value.map(m => ({
    role: m.role,
    content: m.content
  }))
})

// 方法
async function sendMessage(text?: string) {
  const messageText = text || inputMessage.value.trim()
  if (!messageText || isLoading.value) return

  inputMessage.value = ''

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: messageText
  })

  await scrollToBottom()
  isLoading.value = true

  try {
    const response = await aiApi.chat(messageText, conversationHistory.value.slice(-6))

    messages.value.push({
      role: 'assistant',
      content: response.response
    })
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'AI 服务暂时不可用，请稍后再试'
    messages.value.push({
      role: 'assistant',
      content: `抱歉，${errorMessage}`
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

async function scrollToBottom() {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

async function runAnalysis() {
  isAnalyzing.value = true
  analysisResult.value = null

  try {
    analysisResult.value = await aiApi.analyze(analysisDays.value)
  } catch (error: any) {
    console.error('分析失败:', error)
  } finally {
    isAnalyzing.value = false
  }
}

async function loadInsights() {
  loadingInsights.value = true

  try {
    const [insightsData, tipsData] = await Promise.all([
      aiApi.getInsights(7),
      aiApi.getHealthTips()
    ])

    insights.value = insightsData
    healthTips.value = tipsData.tips
  } catch (error) {
    console.error('加载洞察失败:', error)
  } finally {
    loadingInsights.value = false
  }
}

function clearChat() {
  messages.value = [{
    role: 'assistant',
    content: '您好！我是震颤卫士 AI 助手，我可以帮助您分析震颤数据、解答健康问题。请问有什么可以帮您的？'
  }]
}

function getRiskColor(risk: string): string {
  switch (risk) {
    case '低': return 'text-mint-600 bg-mint-100'
    case '高': return 'text-red-500 bg-red-100'
    default: return 'text-amber-600 bg-amber-100'
  }
}

// 生命周期
onMounted(async () => {
  // 添加欢迎消息
  messages.value.push({
    role: 'assistant',
    content: '您好！我是震颤卫士 AI 助手，我可以帮助您分析震颤数据、解答健康问题。请问有什么可以帮您的？'
  })

  // 加载洞察和提示
  await loadInsights()
})
</script>

<template>
  <AppLayout>
    <!-- 页面标题 -->
    <div class="mb-8">
      <div class="flex items-center gap-3 mb-2">
        <div class="w-10 h-10 bg-gradient-to-br from-lavender-400 to-lavender-600 rounded-xl flex items-center justify-center shadow-soft">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-800">AI 助手</h1>
          <p class="text-gray-500 text-sm">智能分析和健康建议</p>
        </div>
      </div>
    </div>

    <!-- 标签页切换 -->
    <div class="mb-6">
      <div class="bg-warmGray-100 rounded-2xl p-1.5 inline-flex gap-1">
        <button
          @click="activeTab = 'chat'"
          :class="[
            'px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200',
            activeTab === 'chat'
              ? 'bg-white text-lavender-600 shadow-soft'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            智能问答
          </span>
        </button>
        <button
          @click="activeTab = 'analysis'"
          :class="[
            'px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200',
            activeTab === 'analysis'
              ? 'bg-white text-lavender-600 shadow-soft'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            数据分析
          </span>
        </button>
        <button
          @click="activeTab = 'insights'"
          :class="[
            'px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200',
            activeTab === 'insights'
              ? 'bg-white text-lavender-600 shadow-soft'
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            洞察与建议
          </span>
        </button>
      </div>
    </div>

    <!-- 智能问答 -->
    <div v-if="activeTab === 'chat'" class="card !p-0 flex flex-col h-[calc(100vh-320px)] overflow-hidden">
      <!-- 聊天历史 -->
      <div ref="chatContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="flex animate-fade-in-up"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
          :style="{ animationDelay: `${index * 50}ms` }"
        >
          <!-- AI 头像 -->
          <div v-if="message.role === 'assistant'" class="flex items-start gap-3 max-w-[85%]">
            <div class="w-9 h-9 bg-gradient-to-br from-lavender-400 to-lavender-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-soft">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div class="bg-gradient-to-br from-lavender-50 to-warmGray-50 text-gray-800 rounded-2xl rounded-tl-md px-4 py-3 shadow-sm border border-lavender-100">
              <p class="whitespace-pre-wrap leading-relaxed">{{ message.content }}</p>
            </div>
          </div>

          <!-- 用户消息 -->
          <div v-else class="max-w-[75%]">
            <div class="bg-gradient-to-r from-lavender-500 to-lavender-600 text-white rounded-2xl rounded-tr-md px-4 py-3 shadow-soft">
              <p class="whitespace-pre-wrap">{{ message.content }}</p>
            </div>
          </div>
        </div>

        <!-- 加载动画 -->
        <div v-if="isLoading" class="flex justify-start">
          <div class="flex items-start gap-3">
            <div class="w-9 h-9 bg-gradient-to-br from-lavender-400 to-lavender-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-soft">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div class="bg-lavender-50 rounded-2xl rounded-tl-md px-4 py-3 flex items-center gap-2 border border-lavender-100">
              <div class="flex gap-1">
                <span class="w-2 h-2 bg-lavender-400 rounded-full animate-bounce" style="animation-delay: 0ms;"></span>
                <span class="w-2 h-2 bg-lavender-400 rounded-full animate-bounce" style="animation-delay: 150ms;"></span>
                <span class="w-2 h-2 bg-lavender-400 rounded-full animate-bounce" style="animation-delay: 300ms;"></span>
              </div>
              <span class="text-lavender-600 text-sm">正在思考...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷问题 -->
      <div v-if="messages.length <= 1" class="px-6 pb-4">
        <p class="text-sm text-gray-500 mb-3">您可以问我：</p>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="q in quickQuestions"
            :key="q"
            @click="sendMessage(q)"
            class="px-4 py-2 bg-gradient-to-r from-lavender-50 to-warmGray-50 hover:from-lavender-100 hover:to-warmGray-100 rounded-xl text-sm text-lavender-700 border border-lavender-200 transition-all duration-200 hover:shadow-sm"
          >
            {{ q }}
          </button>
        </div>
      </div>

      <!-- 输入框 -->
      <div class="p-4 border-t border-warmGray-200 bg-warmGray-50">
        <div class="flex gap-3">
          <div class="flex-1 relative">
            <input
              v-model="inputMessage"
              type="text"
              class="input !rounded-xl !py-3 !pr-12"
              placeholder="输入您的问题..."
              @keyup.enter="sendMessage()"
              :disabled="isLoading"
            />
            <button
              @click="sendMessage()"
              :disabled="isLoading || !inputMessage.trim()"
              class="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 flex items-center justify-center rounded-lg bg-gradient-to-r from-lavender-500 to-lavender-600 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-soft transition-all"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <button
            v-if="messages.length > 1"
            @click="clearChat"
            class="btn btn-ghost !px-3"
            title="清空对话"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 数据分析 -->
    <div v-else-if="activeTab === 'analysis'" class="space-y-6">
      <!-- 分析控制 -->
      <div class="card">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 bg-gradient-to-br from-lavender-400 to-lavender-600 rounded-xl flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800">AI 智能分析</h3>
            <p class="text-sm text-gray-500">使用 AI 对您的震颤数据进行深度分析</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-4">
          <div class="flex items-center gap-3 bg-warmGray-50 rounded-xl px-4 py-2">
            <span class="text-sm text-gray-600">分析范围:</span>
            <select v-model="analysisDays" class="bg-transparent border-none text-sm font-medium text-gray-700 focus:outline-none cursor-pointer">
              <option :value="7">最近7天</option>
              <option :value="14">最近14天</option>
              <option :value="30">最近30天</option>
            </select>
          </div>
          <button
            @click="runAnalysis"
            :disabled="isAnalyzing"
            class="btn bg-gradient-to-r from-lavender-500 to-lavender-600 hover:from-lavender-600 hover:to-lavender-700 text-white"
          >
            <svg v-if="isAnalyzing" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ isAnalyzing ? '分析中...' : '开始分析' }}
          </button>
        </div>
      </div>

      <!-- 分析结果 -->
      <div v-if="analysisResult" class="space-y-6">
        <!-- 风险等级 -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-lavender-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-lavender-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-800">分析结果</h3>
            </div>
            <span
              class="px-4 py-1.5 rounded-full text-sm font-medium"
              :class="getRiskColor(analysisResult.risk_level)"
            >
              风险等级: {{ analysisResult.risk_level }}
            </span>
          </div>
          <p class="text-gray-700 leading-relaxed">{{ analysisResult.summary }}</p>
        </div>

        <!-- 关键发现 -->
        <div class="card">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">关键发现</h3>
          </div>
          <ul class="space-y-3">
            <li
              v-for="(finding, index) in analysisResult.key_findings"
              :key="index"
              class="flex items-start gap-3 p-3 bg-primary-50 rounded-xl animate-fade-in-up"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              <div class="w-6 h-6 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4" />
                </svg>
              </div>
              <span class="text-gray-700">{{ finding }}</span>
            </li>
          </ul>
        </div>

        <!-- 建议 -->
        <div class="card">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 bg-mint-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">建议</h3>
          </div>
          <ul class="space-y-3">
            <li
              v-for="(rec, index) in analysisResult.recommendations"
              :key="index"
              class="flex items-start gap-3 p-3 bg-mint-50 rounded-xl animate-fade-in-up"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              <div class="w-6 h-6 bg-mint-100 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                <svg class="w-4 h-4 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="text-gray-700">{{ rec }}</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!isAnalyzing" class="card text-center py-16">
        <div class="w-20 h-20 bg-gradient-to-br from-lavender-100 to-lavender-200 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-lavender-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">开始智能分析</h3>
        <p class="text-gray-500">点击"开始分析"获取 AI 智能分析报告</p>
      </div>
    </div>

    <!-- 洞察与建议 -->
    <div v-else-if="activeTab === 'insights'" class="space-y-6">
      <!-- 加载状态 -->
      <div v-if="loadingInsights" class="flex flex-col items-center justify-center h-64">
        <div class="relative">
          <div class="w-16 h-16 border-4 border-lavender-200 rounded-full"></div>
          <div class="w-16 h-16 border-4 border-lavender-500 border-t-transparent rounded-full animate-spin absolute inset-0"></div>
        </div>
        <p class="text-gray-500 mt-4">加载洞察中...</p>
      </div>

      <template v-else>
        <!-- 数据洞察 -->
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-lavender-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-lavender-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-800">数据洞察</h3>
            </div>
            <button @click="loadInsights" class="btn btn-ghost text-sm">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              刷新
            </button>
          </div>

          <div v-if="insights?.insights.length" class="space-y-3">
            <div
              v-for="(insight, index) in insights.insights"
              :key="index"
              class="flex items-start gap-3 p-4 bg-gradient-to-r from-lavender-50 to-warmGray-50 rounded-xl border border-lavender-100 animate-fade-in-up"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              <div class="w-8 h-8 bg-lavender-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-lavender-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span class="text-gray-700 leading-relaxed">{{ insight }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8">
            <div class="w-12 h-12 bg-warmGray-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-warmGray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
            </div>
            <p class="text-gray-500">暂无数据洞察</p>
          </div>
        </div>

        <!-- 健康提示 -->
        <div class="card">
          <div class="flex items-center gap-2 mb-6">
            <div class="w-8 h-8 bg-mint-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">健康提示</h3>
          </div>
          <div class="space-y-3">
            <div
              v-for="(tip, index) in healthTips"
              :key="index"
              class="flex items-start gap-3 p-4 bg-gradient-to-r from-mint-50 to-warmGray-50 rounded-xl border border-mint-100 animate-fade-in-up"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              <div class="w-8 h-8 bg-mint-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-mint-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span class="text-gray-700 leading-relaxed">{{ tip }}</span>
            </div>
          </div>
        </div>

        <!-- 免责声明 -->
        <div class="bg-gradient-to-r from-amber-50 to-warmGray-50 border border-amber-200 rounded-2xl p-5">
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <p class="font-semibold text-amber-800 mb-1">重要提示</p>
              <p class="text-sm text-amber-700 leading-relaxed">
                AI 助手提供的分析和建议仅供参考，不能替代专业医生的诊断和治疗意见。
                如有任何健康问题，请及时咨询医疗专业人员。
              </p>
            </div>
          </div>
        </div>
      </template>
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
  animation: fade-in-up 0.3s ease-out forwards;
  opacity: 0;
}
</style>
