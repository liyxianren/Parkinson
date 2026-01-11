/**
 * Tremor Guard - Frontend Entry
 * 震颤卫士 - 前端入口
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './styles/main.css'
import './assets/animations.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
