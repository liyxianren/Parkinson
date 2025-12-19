<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
    <!-- Header -->
    <header class="container mx-auto px-4 py-6">
      <nav class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <span class="text-2xl font-bold text-primary-700">震颤卫士</span>
          <span class="text-sm text-gray-500">Tremor Guard</span>
        </div>
        <div class="flex items-center space-x-4">
          <RouterLink to="/login" class="text-gray-600 hover:text-primary-600">
            登录
          </RouterLink>
          <RouterLink to="/register" class="btn btn-primary">
            注册
          </RouterLink>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <main class="container mx-auto px-4 py-16">
      <div class="text-center max-w-3xl mx-auto">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">
          帕金森震颤<br>
          <span class="text-primary-600">智能监测系统</span>
        </h1>
        <p class="text-xl text-gray-600 mb-8">
          基于 FFT 频谱分析的专业震颤检测，结合 AI 智能分析，
          帮助患者和医生更好地了解和管理帕金森病症状。
        </p>
        <div class="flex justify-center space-x-4">
          <RouterLink to="/register" class="btn btn-primary text-lg px-8 py-3">
            立即开始
          </RouterLink>
          <a href="#features" class="btn btn-secondary text-lg px-8 py-3">
            了解更多
          </a>
        </div>
      </div>

      <!-- Features Section -->
      <section id="features" class="mt-24">
        <h2 class="text-3xl font-bold text-center mb-12">核心功能</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="card text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">实时监测</h3>
            <p class="text-gray-600">
              专业级 FFT 频谱分析，精准检测 4-6Hz 帕金森特征性震颤
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="card text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">AI 智能分析</h3>
            <p class="text-gray-600">
              Claude AI 深度分析震颤数据，提供个性化健康建议
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="card text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">专业报告</h3>
            <p class="text-gray-600">
              生成医疗级报告，方便与医生沟通病情变化
            </p>
          </div>
        </div>
      </section>

      <!-- Severity Scale -->
      <section class="mt-24">
        <h2 class="text-3xl font-bold text-center mb-12">震颤严重度分级</h2>
        <div class="card max-w-2xl mx-auto">
          <div class="space-y-4">
            <div class="flex items-center">
              <span class="severity-badge severity-0 w-20 text-center">无震颤</span>
              <span class="ml-4 text-gray-600">RMS &lt; 2.5g - 正常状态</span>
            </div>
            <div class="flex items-center">
              <span class="severity-badge severity-1 w-20 text-center">轻度</span>
              <span class="ml-4 text-gray-600">RMS 2.5-3.0g - 轻微震颤</span>
            </div>
            <div class="flex items-center">
              <span class="severity-badge severity-2 w-20 text-center">中轻度</span>
              <span class="ml-4 text-gray-600">RMS 3.0-3.5g - 需要关注</span>
            </div>
            <div class="flex items-center">
              <span class="severity-badge severity-3 w-20 text-center">中度</span>
              <span class="ml-4 text-gray-600">RMS 3.5-4.0g - 建议就医</span>
            </div>
            <div class="flex items-center">
              <span class="severity-badge severity-4 w-20 text-center">重度</span>
              <span class="ml-4 text-gray-600">RMS &gt; 4.0g - 需要医疗干预</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="container mx-auto px-4 py-8 mt-16 border-t">
      <div class="text-center text-gray-500">
        <p>&copy; 2024 震颤卫士 Tremor Guard. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>
