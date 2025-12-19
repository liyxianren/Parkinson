<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-9xl font-bold text-gray-200">404</h1>
      <p class="text-2xl font-semibold text-gray-700 mt-4">页面未找到</p>
      <p class="text-gray-500 mt-2">抱歉，您访问的页面不存在</p>
      <RouterLink to="/" class="btn btn-primary mt-8 inline-block">
        返回首页
      </RouterLink>
    </div>
  </div>
</template>
