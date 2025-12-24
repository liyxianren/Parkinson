<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

// 根据路由深度和方向决定过渡动画
const transitionName = computed(() => {
  // 可以根据需要实现更复杂的过渡逻辑
  return 'fade-up'
})
</script>

<template>
  <RouterView v-slot="{ Component, route: currentRoute }">
    <Transition :name="transitionName" mode="out-in">
      <component :is="Component" :key="currentRoute.path" />
    </Transition>
  </RouterView>
</template>

<style>
/* 全局页面过渡样式已在 main.css 中定义 */
</style>
