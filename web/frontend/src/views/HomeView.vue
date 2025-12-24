<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'

const isVisible = ref(false)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})
</script>

<template>
  <div class="min-h-screen bg-warmGray-50 overflow-hidden">
    <!-- Decorative Background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="floating-decoration w-[500px] h-[500px] bg-primary-200/40 -top-64 -right-64" style="animation-delay: 0s;"></div>
      <div class="floating-decoration w-[300px] h-[300px] bg-primary-100/50 top-1/2 -left-32" style="animation-delay: 2s;"></div>
      <div class="floating-decoration w-[400px] h-[400px] bg-lavender-100/30 bottom-0 right-1/3" style="animation-delay: 4s;"></div>
      <div class="floating-decoration w-[200px] h-[200px] bg-mint-100/40 top-1/4 right-1/4" style="animation-delay: 3s;"></div>
    </div>

    <!-- Header -->
    <header class="relative z-10 container mx-auto px-4 py-6">
      <nav class="glass rounded-2xl px-6 py-4 flex items-center justify-between">
        <RouterLink to="/" class="flex items-center space-x-3 group">
          <div class="w-10 h-10 bg-gradient-to-br from-primary-400 to-primary-600 rounded-xl shadow-soft flex items-center justify-center transform transition-transform group-hover:scale-105 group-hover:rotate-3">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <div>
            <span class="text-xl font-bold text-gradient">震颤卫士</span>
            <p class="text-xs text-gray-400">Tremor Guard</p>
          </div>
        </RouterLink>
        <div class="flex items-center gap-3">
          <RouterLink to="/login" class="btn btn-ghost">
            登录
          </RouterLink>
          <RouterLink to="/register" class="btn btn-primary">
            免费注册
          </RouterLink>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <main class="relative z-10 container mx-auto px-4 pt-12 pb-24">
      <div
        :class="[
          'text-center max-w-4xl mx-auto transition-all duration-1000 ease-out',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        ]"
      >
        <!-- Hero Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 rounded-full mb-8">
          <span class="w-2 h-2 bg-mint-500 rounded-full animate-pulse"></span>
          <span class="text-sm font-medium text-primary-700">专业级帕金森震颤监测</span>
        </div>

        <!-- Main Title -->
        <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
          守护健康，<br>
          <span class="text-gradient">智能监测每一刻</span>
        </h1>

        <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
          基于先进的 FFT 频谱分析技术，结合 Claude AI 智能分析，
          为帕金森患者和医疗团队提供精准、温暖的健康守护。
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row justify-center gap-4 mb-16">
          <RouterLink to="/register" class="btn btn-primary btn-lg shadow-glow">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>立即开始</span>
          </RouterLink>
          <a href="#features" class="btn btn-secondary btn-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>了解更多</span>
          </a>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-6 max-w-lg mx-auto">
          <div class="text-center">
            <div class="text-3xl font-bold text-gradient">4-6Hz</div>
            <div class="text-sm text-gray-500">精准检测频率</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gradient">24/7</div>
            <div class="text-sm text-gray-500">全天候监测</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gradient">AI</div>
            <div class="text-sm text-gray-500">智能分析</div>
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <section
        id="features"
        :class="[
          'mt-32 transition-all duration-1000 delay-300',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        ]"
      >
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">核心功能</h2>
          <p class="text-gray-600 max-w-xl mx-auto">
            我们用科技和温暖，为您的健康保驾护航
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="card-gradient text-center group cursor-pointer">
            <div class="w-20 h-20 bg-gradient-to-br from-primary-400 to-primary-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-soft group-hover:shadow-glow transition-all duration-300 group-hover:scale-105">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-3">实时监测</h3>
            <p class="text-gray-600 leading-relaxed">
              专业级 FFT 频谱分析技术，精准检测 4-6Hz 帕金森特征性震颤频率
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="card-gradient text-center group cursor-pointer">
            <div class="w-20 h-20 bg-gradient-to-br from-lavender-400 to-lavender-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-soft group-hover:shadow-glow transition-all duration-300 group-hover:scale-105">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-3">AI 智能分析</h3>
            <p class="text-gray-600 leading-relaxed">
              Claude AI 深度分析震颤数据，提供个性化健康建议和趋势预测
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="card-gradient text-center group cursor-pointer">
            <div class="w-20 h-20 bg-gradient-to-br from-mint-400 to-mint-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-soft group-hover:shadow-glow transition-all duration-300 group-hover:scale-105">
              <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-3">专业报告</h3>
            <p class="text-gray-600 leading-relaxed">
              生成医疗级分析报告，帮助您与医生更好地沟通病情变化
            </p>
          </div>
        </div>
      </section>

      <!-- Severity Scale Section -->
      <section
        :class="[
          'mt-32 transition-all duration-1000 delay-500',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        ]"
      >
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">震颤严重度分级</h2>
          <p class="text-gray-600 max-w-xl mx-auto">
            科学的分级标准，帮助您更好地了解自身状况
          </p>
        </div>

        <div class="card max-w-2xl mx-auto !p-8">
          <div class="space-y-5">
            <div class="flex items-center p-3 rounded-xl hover:bg-green-50 transition-colors">
              <div class="w-24 flex-shrink-0">
                <span class="severity-badge severity-0">无震颤</span>
              </div>
              <div class="flex-1 ml-4">
                <p class="font-medium text-gray-700">RMS &lt; 2.5g</p>
                <p class="text-sm text-gray-500">正常状态，继续保持</p>
              </div>
              <div class="w-16 h-2 bg-green-200 rounded-full overflow-hidden">
                <div class="h-full w-1/5 bg-green-500 rounded-full"></div>
              </div>
            </div>

            <div class="flex items-center p-3 rounded-xl hover:bg-lime-50 transition-colors">
              <div class="w-24 flex-shrink-0">
                <span class="severity-badge severity-1">轻度</span>
              </div>
              <div class="flex-1 ml-4">
                <p class="font-medium text-gray-700">RMS 2.5-3.0g</p>
                <p class="text-sm text-gray-500">轻微震颤，注意观察</p>
              </div>
              <div class="w-16 h-2 bg-lime-200 rounded-full overflow-hidden">
                <div class="h-full w-2/5 bg-lime-500 rounded-full"></div>
              </div>
            </div>

            <div class="flex items-center p-3 rounded-xl hover:bg-yellow-50 transition-colors">
              <div class="w-24 flex-shrink-0">
                <span class="severity-badge severity-2">中轻度</span>
              </div>
              <div class="flex-1 ml-4">
                <p class="font-medium text-gray-700">RMS 3.0-3.5g</p>
                <p class="text-sm text-gray-500">需要关注，建议咨询</p>
              </div>
              <div class="w-16 h-2 bg-yellow-200 rounded-full overflow-hidden">
                <div class="h-full w-3/5 bg-yellow-500 rounded-full"></div>
              </div>
            </div>

            <div class="flex items-center p-3 rounded-xl hover:bg-orange-50 transition-colors">
              <div class="w-24 flex-shrink-0">
                <span class="severity-badge severity-3">中度</span>
              </div>
              <div class="flex-1 ml-4">
                <p class="font-medium text-gray-700">RMS 3.5-4.0g</p>
                <p class="text-sm text-gray-500">建议就医，及时处理</p>
              </div>
              <div class="w-16 h-2 bg-orange-200 rounded-full overflow-hidden">
                <div class="h-full w-4/5 bg-orange-500 rounded-full"></div>
              </div>
            </div>

            <div class="flex items-center p-3 rounded-xl hover:bg-red-50 transition-colors">
              <div class="w-24 flex-shrink-0">
                <span class="severity-badge severity-4">重度</span>
              </div>
              <div class="flex-1 ml-4">
                <p class="font-medium text-gray-700">RMS &gt; 4.0g</p>
                <p class="text-sm text-gray-500">需要医疗干预</p>
              </div>
              <div class="w-16 h-2 bg-red-200 rounded-full overflow-hidden">
                <div class="h-full w-full bg-red-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section
        :class="[
          'mt-32 text-center transition-all duration-1000 delay-700',
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        ]"
      >
        <div class="card-gradient max-w-3xl mx-auto !py-16 !px-8 relative overflow-hidden">
          <!-- Decorative elements -->
          <div class="absolute -top-12 -right-12 w-32 h-32 bg-primary-200/50 rounded-full"></div>
          <div class="absolute -bottom-8 -left-8 w-24 h-24 bg-primary-300/30 rounded-full"></div>

          <div class="relative z-10">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">
              开始您的健康守护之旅
            </h2>
            <p class="text-gray-600 mb-8 max-w-lg mx-auto">
              免费注册，立即体验专业的震颤监测服务
            </p>
            <RouterLink to="/register" class="btn btn-primary btn-lg">
              免费注册
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </RouterLink>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 border-t border-warmGray-200 bg-white/50 backdrop-blur-sm">
      <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <span class="font-semibold text-gray-700">震颤卫士</span>
          </div>
          <p class="text-gray-500 text-sm">
            &copy; 2024 震颤卫士 Tremor Guard · 关爱每一次心跳
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>
