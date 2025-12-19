<script setup lang="ts">
import { ref } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: '您好！我是震颤卫士 AI 助手，我可以帮助您分析震颤数据、解答健康问题。请问有什么可以帮您的？'
  }
])
const inputMessage = ref('')
const isLoading = ref(false)

async function sendMessage() {
  if (!inputMessage.value.trim() || isLoading.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  messages.value.push({
    role: 'user',
    content: userMessage
  })

  isLoading.value = true

  // TODO: 调用 AI API
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: 'AI 功能待实现。这里将会显示 Claude AI 的回复。'
    })
    isLoading.value = false
  }, 1000)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <h1 class="text-2xl font-bold mb-6">AI 助手</h1>

    <div class="card flex flex-col h-[calc(100vh-200px)]">
      <!-- Messages -->
      <div class="flex-1 overflow-y-auto space-y-4 mb-4">
        <div
          v-for="(message, index) in messages"
          :key="index"
          class="flex"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[80%] rounded-lg px-4 py-2"
            :class="message.role === 'user'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 text-gray-800'"
          >
            {{ message.content }}
          </div>
        </div>

        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-gray-100 rounded-lg px-4 py-2 text-gray-500">
            正在思考...
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="flex space-x-2">
        <input
          v-model="inputMessage"
          type="text"
          class="input flex-1"
          placeholder="输入您的问题..."
          @keyup.enter="sendMessage"
        />
        <button
          @click="sendMessage"
          :disabled="isLoading || !inputMessage.trim()"
          class="btn btn-primary"
        >
          发送
        </button>
      </div>
    </div>
  </div>
</template>
