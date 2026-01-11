<script setup lang="ts">



const features = [
  {
    title: '医疗级 MPU6050 传感器',
    desc: '搭载 6 轴运动处理组件，通过 I2C 接口以 100kHz 频率传输数据，精确捕捉每一个微小动作。',
    icon: 'sensor',
    color: 'from-blue-400 to-blue-600'
  },
  {
    title: 'FFT 频谱分析算法',
    desc: '内置高性能数字信号处理芯片，实时执行快速傅里叶变换，精准锁定 4-6Hz 帕金森特征频段。',
    icon: 'fft',
    color: 'from-primary-400 to-primary-600'
  },
  {
    title: 'Claude AI 智能诊断',
    desc: '集成 Anthropic 最新 AI 模型，针对震颤数据生成深度医疗报告，提供个性化康复建议。',
    icon: 'ai',
    color: 'from-purple-400 to-purple-600'
  }
]
</script>

<template>
  <section id="technology" class="py-24 bg-gray-50">
    <div class="container mx-auto px-4">
      <div class="grid lg:grid-cols-3 gap-8">
        <!-- Feature Card -->
        <div 
          v-for="(feature, index) in features" 
          :key="index"
          class="group relative bg-white rounded-3xl p-8 shadow-soft hover:shadow-xl transition-all duration-500 hover:-translate-y-2 overflow-hidden"
        >
          <!-- Gradient Background -->
          <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br opacity-5 rounded-bl-[100px] transition-all group-hover:scale-150 duration-500" :class="feature.color"></div>

          <!-- Icon -->
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br mb-6 flex items-center justify-center transform group-hover:rotate-12 transition-transform duration-500 shadow-md text-white" :class="feature.color">
            <!-- Sensor Icon -->
            <svg v-if="feature.icon === 'sensor'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
            <!-- FFT Icon -->
            <svg v-if="feature.icon === 'fft'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            <!-- AI Icon -->
            <svg v-if="feature.icon === 'ai'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>

          <h3 class="text-2xl font-bold text-gray-900 mb-4">{{ feature.title }}</h3>
          <p class="text-gray-600 leading-relaxed">{{ feature.desc }}</p>
          
          <div class="mt-6 flex items-center text-sm font-semibold transition-colors" :class="feature.color.replace('from-', 'text-').split(' ')[0]">
            了解更多
            <svg class="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
