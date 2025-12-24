/**
 * Tremor Guard - Auth Store
 * 震颤卫士 - 认证状态管理
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isDoctor = computed(() => user.value?.role === 'doctor')

  // Actions
  async function login(email: string, password: string) {
    loading.value = true
    error.value = null

    try {
      const response = await authApi.login(email, password)
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || '登录失败'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(email: string, username: string, password: string, fullName?: string) {
    loading.value = true
    error.value = null

    try {
      const response = await authApi.register({ email, username, password, full_name: fullName })
      // 注册成功后自动登录
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      return true
    } catch (e: any) {
      error.value = e.response?.data?.detail || '注册失败'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return

    try {
      user.value = await authApi.getCurrentUser()
    } catch (e) {
      logout()
    }
  }

  async function refreshToken() {
    try {
      const response = await authApi.refreshToken()
      token.value = response.access_token
      user.value = response.user
      localStorage.setItem('token', response.access_token)
      return true
    } catch (e) {
      logout()
      return false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  function clearError() {
    error.value = null
  }

  // 初始化时获取用户信息
  if (token.value) {
    fetchUser()
  }

  return {
    // State
    user,
    token,
    loading,
    error,

    // Getters
    isAuthenticated,
    isAdmin,
    isDoctor,

    // Actions
    login,
    register,
    fetchUser,
    refreshToken,
    logout,
    clearError,
  }
})
