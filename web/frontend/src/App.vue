<script setup lang="ts">
import { RouterView } from 'vue-router'

// 页面过渡动画名称
const transitionName = 'fade-up'
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
