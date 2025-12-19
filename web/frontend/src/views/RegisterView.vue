<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const fullName = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const localError = ref('')

async function handleRegister() {
  localError.value = ''

  if (password.value !== confirmPassword.value) {
    localError.value = '两次输入的密码不一致'
    return
  }

  if (password.value.length < 6) {
    localError.value = '密码长度至少 6 位'
    return
  }

  const success = await authStore.register(
    email.value,
    username.value,
    password.value,
    fullName.value || undefined
  )

  if (success) {
    router.push('/login')
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <RouterLink to="/" class="inline-block">
          <h1 class="text-3xl font-bold text-primary-700">震颤卫士</h1>
          <p class="text-sm text-gray-500">Tremor Guard</p>
        </RouterLink>
      </div>

      <!-- Register Card -->
      <div class="card">
        <h2 class="text-2xl font-bold text-center mb-6">注册</h2>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
              邮箱 <span class="text-red-500">*</span>
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="input"
              placeholder="your@email.com"
            />
          </div>

          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              用户名 <span class="text-red-500">*</span>
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              class="input"
              placeholder="username"
            />
          </div>

          <!-- Full Name -->
          <div>
            <label for="fullName" class="block text-sm font-medium text-gray-700 mb-1">
              姓名
            </label>
            <input
              id="fullName"
              v-model="fullName"
              type="text"
              class="input"
              placeholder="您的姓名 (可选)"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              密码 <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                minlength="6"
                class="input pr-10"
                placeholder="至少 6 位"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              确认密码 <span class="text-red-500">*</span>
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              required
              class="input"
              placeholder="再次输入密码"
            />
          </div>

          <!-- Error Message -->
          <div v-if="localError || authStore.error" class="text-red-600 text-sm text-center">
            {{ localError || authStore.error }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn btn-primary w-full py-3"
          >
            <span v-if="authStore.loading">注册中...</span>
            <span v-else>注册</span>
          </button>
        </form>

        <!-- Login Link -->
        <p class="mt-6 text-center text-gray-600">
          已有账号?
          <RouterLink to="/login" class="text-primary-600 hover:text-primary-700 font-medium">
            立即登录
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>
