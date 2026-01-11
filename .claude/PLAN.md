# Tremor Guard 前端开发进度总计划

> 震颤卫士 - AI增强版帕金森震颤监测系统前端功能开发计划
> 创建时间：2026-01-04
> 最后更新：2026-01-04

---

## 项目概述

根据《帕金森震颤监测手环_AI增强版_项目招生介绍》文档需求，本计划涵盖4个新功能模块的前端开发：

| 模块 | 状态 | 说明 |
|------|------|------|
| 用药关联 | ✅ 核心完成 | 记录服药时间，分析药效周期与震颤关系 |
| 健康档案 | ✅ 核心完成 | 患者基本信息、病历记录、家族病史、就诊记录 |
| 运动康复 | ✅ 核心完成 | 康复训练计划、运动指导、训练打卡记录 |
| AI医生增强 | ✅ 核心完成 | 数据解读、个性化建议、就诊报告AI摘要 |

**状态说明**：⬜ 待开发 | 🟡 进行中 | ✅ 已完成

---

## 模块一：用药关联模块

### 功能描述
- 用药记录管理（添加、编辑、删除药物）
- 服药提醒设置
- 药效周期分析图表（服药时间 vs 震颤严重度）
- 药效波动规律识别

### 关键文件
- `web/frontend/src/views/MedicationView.vue` - 主页面（新建）
- `web/frontend/src/api/medication.ts` - API 模块（新建）
- `web/frontend/src/stores/medication.ts` - 状态管理（新建）
- `web/frontend/src/types/index.ts` - 类型定义（扩展）
- `web/frontend/src/router/index.ts` - 路由配置（扩展）
- `web/frontend/src/layouts/AppLayout.vue` - 侧边栏菜单（扩展）

### 任务清单

| # | 任务 | 状态 | 备注 |
|---|------|------|------|
| 1.1 | 创建 Medication 类型定义 | ✅ | types/index.ts |
| 1.2 | 创建 medication.ts API 模块 | ✅ | api/medication.ts |
| 1.3 | 创建 medication.ts Store | ✅ | stores/medication.ts |
| 1.4 | 添加路由配置和侧边栏菜单 | ✅ | router + AppLayout |
| 1.5 | 创建 MedicationView.vue 主页面骨架 | ✅ | 含 4 个 Tab |
| 1.6 | 实现药物列表 Tab（CRUD） | ✅ | 药物管理 |
| 1.7 | 实现 MedicationCard 和 MedicationForm 组件 | ✅ | 内联实现 |
| 1.8 | 实现服药记录 Tab | ✅ | 服药历史 |
| 1.9 | 实现今日服药提醒卡片 | ✅ | 待服药列表 |
| 1.10 | 实现药效分析图表 | ✅ | Chart.js 图表 |
| 1.11 | 实现提醒设置功能 | ✅ | 基础配置界面 |
| 1.12 | Dashboard 集成服药提醒组件 | ⬜ | 首页集成 |

---

## 模块二：健康档案模块

### 功能描述
- 个人健康档案（年龄、确诊时间、Hoehn-Yahr分期等）
- 病历管理（症状记录、诊断记录）
- 家族病史记录
- 就诊记录管理（时间、医院、医生、诊断、处方）

### 关键文件
- `web/frontend/src/views/HealthProfileView.vue` - 主页面（新建）
- `web/frontend/src/api/health.ts` - API 模块（新建）
- `web/frontend/src/stores/health.ts` - 状态管理（新建）
- `web/frontend/src/types/index.ts` - 类型定义（扩展）

### 任务清单

| # | 任务 | 状态 | 备注 |
|---|------|------|------|
| 2.1 | 创建 Health 类型定义 | ✅ | types/index.ts |
| 2.2 | 创建 health.ts API 模块 | ✅ | api/health.ts |
| 2.3 | 创建 health.ts Store | ✅ | stores/health.ts |
| 2.4 | 添加路由配置和侧边栏菜单 | ✅ | router + AppLayout |
| 2.5 | 创建 HealthProfileView.vue 主页面骨架 | ✅ | 含 4 个 Tab |
| 2.6 | 实现个人健康档案 Tab | ✅ | 基本信息表单 |
| 2.7 | 实现 ProfileEditForm 组件（含 H-Y 分期选择） | ✅ | 内联实现 |
| 2.8 | 实现病历记录 Tab（列表+表单） | ✅ | 病历 CRUD |
| 2.9 | 实现家族病史 Tab | ✅ | 家族史管理 |
| 2.10 | 实现就诊记录 Tab（含处方记录） | ✅ | 就诊记录 CRUD |
| 2.11 | 实现附件上传功能 | ✅ | 病历/就诊附件上传 |
| 2.12 | 实现复诊提醒功能 | ✅ | 复诊日期提醒 |

---

## 模块三：运动康复模块

### 功能描述
- 康复训练库（推荐的康复动作/视频）
- 个人训练计划管理
- 每日训练打卡
- 训练进度追踪统计

### 关键文件
- `web/frontend/src/views/RehabilitationView.vue` - 主页面（新建）
- `web/frontend/src/api/rehabilitation.ts` - API 模块（新建）
- `web/frontend/src/stores/rehabilitation.ts` - 状态管理（新建）
- `web/frontend/src/types/index.ts` - 类型定义（扩展）

### 任务清单

| # | 任务 | 状态 | 备注 |
|---|------|------|------|
| 3.1 | 创建 Rehabilitation 类型定义 | ✅ | types/index.ts |
| 3.2 | 创建 rehabilitation.ts API 模块 | ✅ | api/rehabilitation.ts |
| 3.3 | 创建 rehabilitation.ts Store | ✅ | stores/rehabilitation.ts |
| 3.4 | 添加路由配置和侧边栏菜单 | ✅ | router + AppLayout |
| 3.5 | 创建 RehabilitationView.vue 主页面骨架 | ✅ | 含 4 个 Tab |
| 3.6 | 实现训练库 Tab（动作卡片列表+筛选） | ✅ | 运动库浏览 |
| 3.7 | 实现 ExerciseCard 和 ExerciseDetail 组件 | ✅ | 内联实现 |
| 3.8 | 实现视频播放组件 | ⬜ | 视频指导（待后端支持） |
| 3.9 | 实现我的计划 Tab（计划管理） | ✅ | 计划 CRUD |
| 3.10 | 实现 TrainingPlanEditor 组件 | ✅ | 内联实现 |
| 3.11 | 实现训练打卡 Tab（打卡流程） | ✅ | 每日打卡 |
| 3.12 | 实现 WeeklyCalendar 日历组件 | ✅ | 内联实现 |
| 3.13 | 实现进度统计 Tab（图表） | ✅ | 基础统计展示 |
| 3.14 | Dashboard 集成今日训练提醒 | ⬜ | 首页集成 |

---

## 模块四：AI医生功能增强

### 功能描述
- 震颤数据智能解读（自动分析今日数据，生成通俗报告）
- 症状问答与健康咨询（支持多类型问答）
- 个性化健康建议（基于历史数据、用药记录、生活习惯）
- 就诊报告AI摘要（生成数据摘要供医生参考）
- 用药关联分析建议

### 关键文件
- `web/frontend/src/views/AIAssistantView.vue` - 现有页面（重构扩展）
- `web/frontend/src/api/ai.ts` - API 模块（扩展）
- `web/frontend/src/types/index.ts` - 类型定义（扩展）

### 任务清单

| # | 任务 | 状态 | 备注 |
|---|------|------|------|
| 4.1 | 扩展 AI 类型定义 | ✅ | types/index.ts |
| 4.2 | 扩展 ai.ts API 模块 | ✅ | api/ai.ts |
| 4.3 | 重构 AIAssistantView 添加新 Tab | ✅ | 页面结构调整 |
| 4.4 | 实现今日解读 Tab | ✅ | 每日数据解读 |
| 4.5 | 实现 DailyAnalysisCard 组件 | ✅ | 解读卡片（内联实现） |
| 4.6 | 实现个性化建议展示 | ✅ | 建议列表 |
| 4.7 | 实现就诊报告生成器 Tab | ✅ | 报告生成界面 |
| 4.8 | 实现 DoctorReportGenerator 组件 | ✅ | 报告生成逻辑（内联实现） |
| 4.9 | 实现报告 PDF 导出功能 | ⬜ | PDF 导出 |
| 4.10 | 增强智能问答上下文感知 | ⬜ | 上下文对话 |
| 4.11 | 实现症状自查功能 | ✅ | 症状检查 |
| 4.12 | 实现用药关联分析展示 | ⬜ | 药效分析展示 |
| 4.13 | Dashboard 集成 AI 今日提示 | ⬜ | 首页集成 |

---

## 开发顺序建议

### 阶段一：基础架构 ✅ 已完成
**目标**：搭建所有模块的基础代码结构

1. ✅ 所有模块的类型定义（1.1, 2.1, 3.1, 4.1）
2. ✅ 所有模块的 API 模块（1.2, 2.2, 3.2, 4.2）
3. ✅ 所有模块的 Store（1.3, 2.3, 3.3）
4. ✅ 路由和侧边栏更新（1.4, 2.4, 3.4）
5. ✅ 所有页面骨架创建（1.5, 2.5, 3.5, 4.3）

### 阶段二：核心功能 ✅ 已完成
**目标**：实现各模块的主要功能

1. ✅ 用药关联模块核心（1.6-1.9）
2. ✅ 健康档案模块核心（2.6-2.10）
3. ✅ 运动康复模块核心（3.6-3.13，除视频播放）
4. ✅ AI增强核心功能（4.4-4.8）

### 阶段三：进阶功能
**目标**：完善图表、报告、集成等功能

1. ⬜ 药效分析图表（1.10-1.11）
2. ⬜ 就诊记录与附件（2.10-2.12）
3. ⬜ 训练统计图表（3.12-3.14）
4. ⬜ AI报告导出与集成（4.9-4.13）

### 阶段四：集成优化
**目标**：Dashboard 集成、UI优化、测试

1. ⬜ Dashboard 集成所有模块提示（1.12, 3.14, 4.13）
2. ⬜ UI/UX 优化
3. ⬜ 响应式适配
4. ⬜ 端到端测试

---

## 技术规范

### 代码风格
- Vue 组件使用 `<script setup lang="ts">` + Composition API
- API 模块独立文件，统一导出
- Store 使用 Pinia + Composition API
- 样式使用 Tailwind CSS，遵循现有主题（温暖橙色）

### 目录结构
```
web/frontend/src/
├── api/
│   ├── medication.ts     # ✅ 已创建
│   ├── health.ts         # ✅ 已创建
│   └── rehabilitation.ts # ✅ 已创建
├── stores/
│   ├── medication.ts     # ✅ 已创建
│   ├── health.ts         # ✅ 已创建
│   └── rehabilitation.ts # ✅ 已创建
├── views/
│   ├── MedicationView.vue      # ✅ 已创建
│   ├── HealthProfileView.vue   # ✅ 已创建
│   ├── RehabilitationView.vue  # ✅ 已创建
│   └── AIAssistantView.vue     # ✅ 已重构
├── components/
│   ├── medication/       # 待开发
│   ├── health/           # 待开发
│   ├── rehab/            # 待开发
│   └── ai/               # 待开发
└── types/
    └── index.ts          # ✅ 已扩展
```

---

## 进度统计

| 模块 | 总任务 | 已完成 | 进度 |
|------|--------|--------|------|
| 用药关联 | 12 | 9 | 75% |
| 健康档案 | 12 | 12 | 100% |
| 运动康复 | 14 | 12 | 86% |
| AI医生增强 | 13 | 9 | 69% |
| **总计** | **51** | **40** | **78%** |

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-01-04 | 创建初始计划文档 |
| 2026-01-04 | 完成阶段一：基础架构（类型定义、API、Store、路由、页面骨架） |
| 2026-01-04 | 完成 AI 医生增强核心功能（今日解读、就诊报告、症状自查） |
| 2026-01-04 | 完成用药关联模块核心功能（药物CRUD、服药记录、今日提醒） |
| 2026-01-04 | 完成健康档案模块核心功能（档案编辑、病历、家族史、就诊记录） |
| 2026-01-04 | 完成运动康复模块核心功能（训练库、计划管理、打卡、周历、统计） |
