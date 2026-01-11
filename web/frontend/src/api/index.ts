/**
 * Tremor Guard - API Client
 * 震颤卫士 - API 客户端
 */

import axios from 'axios'
import type { AxiosInstance } from 'axios'

// 创建 axios 实例
const apiClient: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证 token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // 401 未授权 - token 过期
    if (error.response?.status === 401) {
      // 如果是登录接口本身的 401 错误，不进行跳转，直接返回错误让组件处理
      if (error.config.url?.includes('/auth/login')) {
        return Promise.reject(error)
      }

      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
