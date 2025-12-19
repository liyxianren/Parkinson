/**
 * Tremor Guard - Vue Router
 * 震颤卫士 - 路由配置
 */

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录', guest: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { title: '注册', guest: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { title: '仪表盘', requiresAuth: true }
  },
  {
    path: '/monitor',
    name: 'monitor',
    component: () => import('@/views/MonitorView.vue'),
    meta: { title: '实时监测', requiresAuth: true }
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('@/views/HistoryView.vue'),
    meta: { title: '历史记录', requiresAuth: true }
  },
  {
    path: '/analysis',
    name: 'analysis',
    component: () => import('@/views/AnalysisView.vue'),
    meta: { title: '数据分析', requiresAuth: true }
  },
  {
    path: '/ai-assistant',
    name: 'ai-assistant',
    component: () => import('@/views/AIAssistantView.vue'),
    meta: { title: 'AI 助手', requiresAuth: true }
  },
  {
    path: '/devices',
    name: 'devices',
    component: () => import('@/views/DevicesView.vue'),
    meta: { title: '设备管理', requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'reports',
    component: () => import('@/views/ReportsView.vue'),
    meta: { title: '报告中心', requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/SettingsView.vue'),
    meta: { title: '设置', requiresAuth: true }
  },
  {
    path: '/test',
    name: 'test',
    component: () => import('@/views/TestView.vue'),
    meta: { title: 'ESP32 测试' }
  },
  {
    path: '/config',
    name: 'config',
    component: () => import('@/views/ConfigView.vue'),
    meta: { title: '参数配置' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '震颤卫士'} | Tremor Guard`

  // TODO: 添加认证检查
  // const authStore = useAuthStore()
  // if (to.meta.requiresAuth && !authStore.isAuthenticated) {
  //   next({ name: 'login', query: { redirect: to.fullPath } })
  // } else if (to.meta.guest && authStore.isAuthenticated) {
  //   next({ name: 'dashboard' })
  // } else {
  //   next()
  // }

  next()
})

export default router
