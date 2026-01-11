# 帕金森震颤监测手环 - 开发文档
# Tremor Guard - Development Guide

**项目名称 / Project Name**: 震颤卫士 (Tremor Guard)
**版本 / Version**: 1.0
**最后更新 / Last Updated**: 2024年12月

---

## 目录 (Table of Contents)

- [第一部分：项目概述 (Project Overview)](#第一部分项目概述-project-overview)
- [第二部分：硬件模块 (Hardware Module)](#第二部分硬件模块-hardware-module)
- [第三部分：后端服务 (Backend Service)](#第三部分后端服务-backend-service)
- [第四部分：前端网站 (Frontend Website)](#第四部分前端网站-frontend-website)
- [第五部分：AI 医生模块 (AI Doctor Module)](#第五部分ai-医生模块-ai-doctor-module)
- [第六部分：数据流设计 (Data Flow Design)](#第六部分数据流设计-data-flow-design)
- [第七部分：开发任务清单 (Development Checklist)](#第七部分开发任务清单-development-checklist)
- [附录 (Appendix)](#附录-appendix)

---

# 第一部分：项目概述 (Project Overview)

## 1.1 项目简介 (Project Introduction)

**震颤卫士 (Tremor Guard)** 是一款面向帕金森病患者的智能可穿戴设备系统，通过实时监测手部震颤数据，结合 AI 智能分析，为患者提供居家健康管理服务。

### 核心功能 (Core Features)

| 功能模块 | 功能描述 | 技术实现 |
|---------|---------|---------|
| **震颤检测** | 实时采集手部运动数据，识别 4-6Hz 帕金森特征性震颤 | FFT 频谱分析 |
| **严重度量化** | 计算震颤频率、幅度、持续时间等指标 | 特征提取算法 |
| **趋势追踪** | 每日/每周/每月震颤变化曲线 | 时序数据库 + 可视化 |
| **用药关联** | 记录服药时间，分析药效周期与震颤的关系 | 数据关联分析 |
| **AI 医生** | 智能健康咨询、数据解读、个性化建议 | LLM + RAG |
| **报告生成** | 导出 PDF 报告供就诊使用 | 自动化报告模板 |

---

## 1.2 系统架构 (System Architecture)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              系统整体架构                                     │
│                         System Architecture                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   硬件层    │    │    后端层     │    │    AI层     │    │   前端层    │ │
│  │  Hardware   │    │   Backend    │    │     AI      │    │  Frontend   │ │
│  ├─────────────┤    ├──────────────┤    ├─────────────┤    ├─────────────┤ │
│  │             │    │              │    │             │    │             │ │
│  │ ESP32-C3    │    │ FastAPI/     │    │ Claude API  │    │ Vue 3 +     │ │
│  │ +           │───►│ Express      │───►│ +           │───►│ TypeScript  │ │
│  │ MPU6050     │WiFi│ +            │    │ RAG         │    │ +           │ │
│  │             │    │ PostgreSQL/  │    │ 知识库      │    │ Tailwind    │ │
│  │             │    │ MongoDB      │    │             │    │             │ │
│  └─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘ │
│                                                                             │
│                            ▼ 数据流向 Data Flow ▼                           │
│                                                                             │
│   传感器数据 ──► WiFi上传 ──► 数据存储 ──► 震颤分析 ──► AI解读 ──► 用户界面  │
│   Sensor Data    Upload     Storage     Analysis    AI         UI Display  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.3 技术栈清单 (Technology Stack)

### 硬件 (Hardware)
| 组件 | 型号/技术 | 用途 |
|-----|----------|------|
| 主控芯片 | Seeed XIAO ESP32-C3 | 数据采集、WiFi 传输 |
| 运动传感器 | MPU6050 (6轴 IMU) | 三轴加速度 + 三轴陀螺仪 |
| 电源 | 3.7V 锂电池 500mAh | 供电 |
| 充电模块 | TP4056 | Type-C 充电管理 |

### 后端 (Backend)
| 技术 | 用途 |
|-----|------|
| Python 3.10+ / Node.js 18+ | 运行环境 |
| FastAPI / Express.js | Web 框架 |
| PostgreSQL / MongoDB | 数据库 |
| Redis | 缓存 + 实时数据 |
| WebSocket | 实时数据推送 |
| NumPy + SciPy | FFT 频谱分析 |

### 前端 (Frontend)
| 技术 | 用途 |
|-----|------|
| Vue 3 | UI 框架 |
| TypeScript | 类型安全 |
| Tailwind CSS | 样式 |
| Chart.js / Vue-Chartjs | 数据可视化 |
| Axios | HTTP 请求 |
| Socket.IO Client | WebSocket 通信 |

### AI (Artificial Intelligence)
| 技术 | 用途 |
|-----|------|
| Claude API (Anthropic) | 大语言模型 |
| LangChain / LlamaIndex | RAG 框架 |
| Chroma / Pinecone | 向量数据库 |

---

# 第二部分：硬件模块 (Hardware Module)

## 2.1 硬件清单 (Bill of Materials / BOM)

| 序号 | 组件名称 | 型号规格 | 数量 | 参考价格 | 备注 |
|-----|---------|---------|-----|---------|------|
| 1 | 主控板 | Seeed XIAO ESP32-C3 | 1 | ¥35 | 带 WiFi/BLE |
| 2 | 传感器 | MPU6050 模块 | 1 | ¥10 | 6轴 IMU |
| 3 | 锂电池 | 3.7V 500mAh | 1 | ¥15 | 带保护板 |
| 4 | 充电模块 | TP4056 Type-C | 1 | ¥5 | 1A 充电 |
| 5 | 开关 | 滑动开关 | 1 | ¥1 | 电源控制 |
| 6 | 导线 | 硅胶线 | 若干 | ¥5 | 连接用 |
| 7 | 外壳 | 3D 打印腕带式 | 1 | ¥30 | 可选 |

**硬件总成本 / Total Cost**: 约 ¥100

---

## 2.2 电路连接 (Circuit Connection)

### 接线图 (Wiring Diagram)

```
                    Seeed XIAO ESP32-C3
                   ┌─────────────────────┐
                   │                     │
    MPU6050        │  D4 (GPIO6) ◄──────┼───── SDA (绿色)
    ┌────────┐     │  D5 (GPIO7) ◄──────┼───── SCL (绿色)
    │ VCC ───┼─────┼── 3V3              │
    │ GND ───┼─────┼── GND              │
    │ SDA ───┼─────┼── D4 (GPIO6)       │
    │ SCL ───┼─────┼── D5 (GPIO7)       │
    │ INT ───┼─────┼── D3 (GPIO5) [可选] │
    │ AD0 ───┼─────┼── GND (地址=0x68)  │
    └────────┘     │                     │
                   └─────────────────────┘

    电源部分:
    ┌────────┐     ┌────────┐     ┌────────────┐
    │ 锂电池  │────►│ TP4056 │────►│ ESP32-C3   │
    │ 3.7V   │     │ 充电板  │     │ 3V3/GND    │
    └────────┘     └────────┘     └────────────┘
```

### 引脚对照表 (Pin Mapping)

| XIAO ESP32-C3 引脚 | GPIO | MPU6050 引脚 | 功能说明 |
|-------------------|------|-------------|---------|
| D4 | GPIO6 | SDA | I2C 数据线 |
| D5 | GPIO7 | SCL | I2C 时钟线 |
| D3 | GPIO5 | INT | 中断引脚 (可选) |
| 3V3 | - | VCC, VLOGIC | 电源 3.3V |
| GND | - | GND | 地线 |

---

## 2.3 MPU6050 传感器规格 (Sensor Specifications)

### 基本参数 (Basic Parameters)

| 参数 | 数值 | 说明 |
|-----|------|------|
| 工作电压 | 3.3V (兼容 5V) | 使用 3.3V 供电 |
| I2C 地址 | 0x68 (AD0=LOW) | AD0 接地时 |
| I2C 速率 | 100kHz / 400kHz | 标准/快速模式 |

### 加速度计 (Accelerometer)

| 量程 | 灵敏度 | 配置值 | 适用场景 |
|-----|-------|-------|---------|
| ±2g | 16384 LSB/g | 0x00 | **震颤检测 (推荐)** |
| ±4g | 8192 LSB/g | 0x08 | 一般运动 |
| ±8g | 4096 LSB/g | 0x10 | 剧烈运动 |
| ±16g | 2048 LSB/g | 0x18 | 冲击检测 |

### 陀螺仪 (Gyroscope)

| 量程 | 灵敏度 | 配置值 | 适用场景 |
|-----|-------|-------|---------|
| ±250°/s | 131 LSB/°/s | 0x00 | **震颤检测 (推荐)** |
| ±500°/s | 65.5 LSB/°/s | 0x08 | 一般旋转 |
| ±1000°/s | 32.8 LSB/°/s | 0x10 | 快速旋转 |
| ±2000°/s | 16.4 LSB/°/s | 0x18 | 极速旋转 |

### 帕金森震颤检测推荐配置 (Recommended Config for Tremor Detection)

```c
// 采样率: 125Hz (足够捕捉 4-6Hz 震颤)
SMPLRT_DIV = 7;        // 采样率 = 1kHz / (1+7) = 125Hz

// 数字低通滤波器: 44Hz 带宽
CONFIG = 0x03;         // DLPF_CFG = 3, 带宽 44Hz

// 加速度计: ±2g (高灵敏度)
ACCEL_CONFIG = 0x00;   // AFS_SEL = 0

// 陀螺仪: ±250°/s (高灵敏度)
GYRO_CONFIG = 0x00;    // FS_SEL = 0
```

---

## 2.4 已完成功能 (Completed Features)

基于 `mpu6050_init/mpu6050_init/mpu6050_init.ino` 代码，以下功能已实现并测试通过：

### 2.4.1 I2C 通信初始化 (I2C Initialization)

```cpp
// 引脚配置
#define I2C_SDA_PIN     6       // GPIO6 -> MPU6050 SDA
#define I2C_SCL_PIN     7       // GPIO7 -> MPU6050 SCL
#define I2C_CLOCK_SPEED 100000  // 100kHz 标准模式

// 初始化代码
Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
Wire.setClock(I2C_CLOCK_SPEED);
```

**状态**: ✅ 已完成

### 2.4.2 设备识别与验证 (Device Identification)

- I2C 总线扫描 (地址范围 0x01-0x7F)
- WHO_AM_I 寄存器验证 (返回值 0x68 = MPU6050)
- 兼容 MPU6500 (0x70) 和 MPU9250 (0x71)

**状态**: ✅ 已完成

### 2.4.3 传感器配置 (Sensor Configuration)

| 配置项 | 设置值 | 说明 |
|-------|-------|------|
| 时钟源 | PLL with X Gyro | 高精度 |
| 采样率 | 125Hz | SMPLRT_DIV = 7 |
| DLPF 带宽 | 44Hz | CONFIG = 0x03 |
| 加速度计量程 | ±2g | ACCEL_CONFIG = 0x00 |
| 陀螺仪量程 | ±250°/s | GYRO_CONFIG = 0x00 |

**状态**: ✅ 已完成

### 2.4.4 数据读取 (Data Reading)

- 连续读取 14 字节数据 (从 0x3B 开始)
- 数据格式: 加速度 XYZ + 温度 + 陀螺仪 XYZ
- 物理值转换:
  - 加速度: `raw / 16384.0` → g
  - 陀螺仪: `raw / 131.0` → °/s
  - 温度: `raw / 340.0 + 36.53` → °C

**状态**: ✅ 已完成

### 2.4.5 串口命令系统 (Serial Command System)

| 命令 | 功能 | 说明 |
|-----|------|------|
| `test` | 运行完整硬件测试 | I2C扫描 + 初始化 + 数据读取 |
| `scan` | 扫描 I2C 总线 | 发现所有 I2C 设备 |
| `read` | 读取一次传感器数据 | 显示原始值和物理值 |
| `stream` | 连续数据输出模式 | 10Hz 输出 (用于调试) |
| `reset` | 复位 MPU6050 | 软件复位 |
| `help` | 显示帮助信息 | 命令列表 |

**状态**: ✅ 已完成

---

## 2.5 待开发功能 (Features to Develop)

### 2.5.1 WiFi 数据上传 (WiFi Data Upload)

**功能描述**: 通过 WiFi 将传感器数据实时上传到云端服务器

**技术方案**:
```cpp
// WiFi 连接
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://your-server.com/api/data/upload";

// 数据上传 (HTTP POST)
void uploadData(int16_t* accel, int16_t* gyro, int16_t temp) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"accel\":[" + String(accel[0]) + "," +
                  String(accel[1]) + "," + String(accel[2]) + "]," +
                  "\"gyro\":[" + String(gyro[0]) + "," +
                  String(gyro[1]) + "," + String(gyro[2]) + "]," +
                  "\"temp\":" + String(temp) + "}";

    int httpCode = http.POST(json);
    http.end();
}
```

**开发状态**: ⏳ 待开发

### 2.5.2 低功耗模式 (Low Power Mode)

**功能描述**: 设备空闲时进入低功耗模式，延长电池续航

**技术方案**:
- MPU6050 运动检测中断唤醒
- ESP32-C3 Deep Sleep 模式
- 预计续航: 24-48 小时

**开发状态**: ⏳ 待开发

### 2.5.3 电池电量监测 (Battery Monitoring)

**功能描述**: 实时监测电池电量，低电量提醒

**技术方案**:
- ADC 读取电池电压
- 电压-电量映射 (3.0V=0%, 4.2V=100%)

**开发状态**: ⏳ 待开发

---

# 第三部分：后端服务 (Backend Service)

## 3.1 技术选型 (Technology Selection)

### 推荐方案 A: Python + FastAPI (已选定 / Selected)

```
优势:
- Python 生态丰富，适合数据处理和 AI 集成
- FastAPI 高性能，自动生成 API 文档
- NumPy/SciPy 便于实现 FFT 分析

技术栈:
- 框架: FastAPI
- 数据库: PostgreSQL + Redis
- ORM: SQLAlchemy
- 数据处理: NumPy, SciPy, Pandas
```

### 备选方案 B: Node.js + Express (已弃用 / Deprecated)

```
优势:
- JavaScript 全栈统一
- 实时通信 (WebSocket) 原生支持好
- 部署简单

技术栈:
- 框架: Express.js
- 数据库: MongoDB + Redis
- ODM: Mongoose
- 数据处理: mathjs
```

---

## 3.2 数据库设计 (Database Design)

### 3.2.1 用户表 (users)

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username        VARCHAR(50) UNIQUE NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    phone           VARCHAR(20),

    -- 患者信息
    birth_date      DATE,
    gender          VARCHAR(10),       -- male/female/other
    diagnosis_date  DATE,              -- 确诊日期
    disease_stage   VARCHAR(20),       -- early/middle/late

    -- 时间戳
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login      TIMESTAMP
);
```

### 3.2.2 设备表 (devices)

```sql
CREATE TABLE devices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    device_id       VARCHAR(50) UNIQUE NOT NULL,  -- 设备唯一标识
    device_name     VARCHAR(100),
    firmware_version VARCHAR(20),

    -- 设备状态
    is_active       BOOLEAN DEFAULT true,
    battery_level   INTEGER,           -- 0-100
    last_seen       TIMESTAMP,

    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2.3 传感器数据表 (sensor_data)

```sql
CREATE TABLE sensor_data (
    id              BIGSERIAL PRIMARY KEY,
    device_id       UUID REFERENCES devices(id),
    timestamp       TIMESTAMP NOT NULL,

    -- 加速度计数据 (原始值)
    accel_x         SMALLINT NOT NULL,
    accel_y         SMALLINT NOT NULL,
    accel_z         SMALLINT NOT NULL,

    -- 陀螺仪数据 (原始值)
    gyro_x          SMALLINT NOT NULL,
    gyro_y          SMALLINT NOT NULL,
    gyro_z          SMALLINT NOT NULL,

    -- 温度
    temperature     SMALLINT,

    -- 索引优化
    INDEX idx_device_time (device_id, timestamp)
);

-- 使用时序数据库扩展 (可选)
-- SELECT create_hypertable('sensor_data', 'timestamp');
```

### 3.2.4 震颤分析结果表 (tremor_analysis)

```sql
CREATE TABLE tremor_analysis (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID REFERENCES users(id),
    device_id           UUID REFERENCES devices(id),

    -- 时间范围
    start_time          TIMESTAMP NOT NULL,
    end_time            TIMESTAMP NOT NULL,
    duration_seconds    INTEGER NOT NULL,

    -- 震颤特征
    tremor_detected     BOOLEAN NOT NULL,
    dominant_frequency  DECIMAL(4,2),      -- 主频 Hz (e.g., 4.50)
    frequency_range_min DECIMAL(4,2),      -- 频率范围下限
    frequency_range_max DECIMAL(4,2),      -- 频率范围上限

    -- 幅度特征
    amplitude_mean      DECIMAL(8,4),      -- 平均幅度 (g)
    amplitude_max       DECIMAL(8,4),      -- 最大幅度
    amplitude_std       DECIMAL(8,4),      -- 幅度标准差

    -- 严重度评估
    severity_score      INTEGER,           -- 0-4 (对应 UPDRS 震颤评分)
    severity_label      VARCHAR(20),       -- none/mild/moderate/severe

    -- 元数据
    analysis_version    VARCHAR(20),       -- 算法版本
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2.5 用药记录表 (medication_records)

```sql
CREATE TABLE medication_records (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),

    -- 药物信息
    medication_name VARCHAR(100) NOT NULL,   -- 药物名称
    dosage          VARCHAR(50),              -- 剂量 (e.g., "100mg")

    -- 服药时间
    taken_at        TIMESTAMP NOT NULL,
    scheduled_at    TIMESTAMP,               -- 计划服药时间

    -- 备注
    notes           TEXT,

    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2.6 AI 对话记录表 (ai_conversations)

```sql
CREATE TABLE ai_conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    session_id      UUID NOT NULL,           -- 会话 ID

    -- 消息内容
    role            VARCHAR(20) NOT NULL,    -- user/assistant/system
    content         TEXT NOT NULL,

    -- 元数据
    tokens_used     INTEGER,
    model_version   VARCHAR(50),

    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3.3 API 接口设计 (API Design)

### 3.3.1 认证接口 (Authentication API)

#### 用户注册 (Register)
```
POST /api/auth/register

Request Body:
{
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "password": "SecurePassword123",
    "phone": "13800138000"
}

Response (201 Created):
{
    "success": true,
    "message": "注册成功",
    "data": {
        "user_id": "uuid-xxx",
        "username": "zhangsan"
    }
}
```

#### 用户登录 (Login)
```
POST /api/auth/login

Request Body:
{
    "email": "zhangsan@example.com",
    "password": "SecurePassword123"
}

Response (200 OK):
{
    "success": true,
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIs...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
        "token_type": "Bearer",
        "expires_in": 3600
    }
}
```

### 3.3.2 设备管理接口 (Device API)

#### 绑定设备 (Bind Device)
```
POST /api/device/bind
Authorization: Bearer <token>

Request Body:
{
    "device_id": "TREMOR-001-ABC123",
    "device_name": "我的手环"
}

Response (200 OK):
{
    "success": true,
    "data": {
        "id": "uuid-xxx",
        "device_id": "TREMOR-001-ABC123",
        "device_name": "我的手环"
    }
}
```

#### 获取设备列表 (Get Devices)
```
GET /api/device/list
Authorization: Bearer <token>

Response (200 OK):
{
    "success": true,
    "data": [
        {
            "id": "uuid-xxx",
            "device_id": "TREMOR-001-ABC123",
            "device_name": "我的手环",
            "is_active": true,
            "battery_level": 85,
            "last_seen": "2024-12-18T10:30:00Z"
        }
    ]
}
```

### 3.3.3 数据上传接口 (Data Upload API)

#### 上传传感器数据 (Upload Sensor Data)
```
POST /api/data/upload
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
    "device_id": "TREMOR-001-ABC123",
    "timestamp": "2024-12-18T10:30:00Z",
    "samples": [
        {
            "t": 0,
            "accel": [1024, -512, 16384],
            "gyro": [10, -5, 3]
        },
        {
            "t": 8,
            "accel": [1030, -508, 16380],
            "gyro": [12, -3, 5]
        }
        // ... 更多采样点 (建议每批次 100-500 个)
    ]
}

Response (200 OK):
{
    "success": true,
    "message": "数据上传成功",
    "data": {
        "samples_received": 100,
        "analysis_triggered": true
    }
}
```

#### 批量上传 (Batch Upload)
```
POST /api/data/upload/batch
Authorization: Bearer <token>
Content-Type: application/octet-stream

Request Body: 二进制数据流 (每个采样 14 字节)

Response (200 OK):
{
    "success": true,
    "samples_received": 1000
}
```

### 3.3.4 数据查询接口 (Data Query API)

#### 实时数据 (WebSocket)
```
WebSocket: ws://your-server.com/ws/realtime
Authorization: Bearer <token>

// 连接后服务器推送实时数据
{
    "type": "sensor_data",
    "timestamp": "2024-12-18T10:30:00.123Z",
    "accel": {"x": 0.062, "y": -0.031, "z": 1.000},
    "gyro": {"x": 0.076, "y": -0.038, "z": 0.023},
    "tremor": {
        "detected": true,
        "frequency": 4.8,
        "amplitude": 0.15
    }
}
```

#### 历史数据查询 (History Query)
```
GET /api/data/history
Authorization: Bearer <token>

Query Parameters:
- start_time: 开始时间 (ISO 8601)
- end_time: 结束时间 (ISO 8601)
- device_id: 设备 ID (可选)
- granularity: 粒度 (raw/minute/hour/day)

Example:
GET /api/data/history?start_time=2024-12-17T00:00:00Z&end_time=2024-12-18T00:00:00Z&granularity=hour

Response (200 OK):
{
    "success": true,
    "data": {
        "time_range": {
            "start": "2024-12-17T00:00:00Z",
            "end": "2024-12-18T00:00:00Z"
        },
        "granularity": "hour",
        "points": [
            {
                "timestamp": "2024-12-17T00:00:00Z",
                "tremor_count": 3,
                "avg_frequency": 4.6,
                "avg_amplitude": 0.12,
                "max_amplitude": 0.25
            },
            // ... 更多数据点
        ]
    }
}
```

### 3.3.5 震颤分析接口 (Tremor Analysis API)

#### 获取分析结果 (Get Analysis)
```
GET /api/analysis/tremor
Authorization: Bearer <token>

Query Parameters:
- date: 日期 (YYYY-MM-DD)
- period: 周期 (day/week/month)

Response (200 OK):
{
    "success": true,
    "data": {
        "period": "day",
        "date": "2024-12-18",
        "summary": {
            "total_tremor_events": 12,
            "total_duration_minutes": 45,
            "dominant_frequency_avg": 4.8,
            "severity_distribution": {
                "mild": 8,
                "moderate": 3,
                "severe": 1
            }
        },
        "events": [
            {
                "id": "uuid-xxx",
                "start_time": "2024-12-18T08:15:00Z",
                "end_time": "2024-12-18T08:18:30Z",
                "duration_seconds": 210,
                "dominant_frequency": 4.6,
                "amplitude_mean": 0.12,
                "severity_score": 1,
                "severity_label": "mild"
            },
            // ... 更多事件
        ]
    }
}
```

### 3.3.6 AI 医生接口 (AI Doctor API)

#### AI 对话 (Chat)
```
POST /api/ai/chat
Authorization: Bearer <token>

Request Body:
{
    "session_id": "uuid-xxx",  // 可选，不传则创建新会话
    "message": "我今天的震颤数据怎么样？",
    "include_context": true    // 是否包含用户数据上下文
}

Response (200 OK):
{
    "success": true,
    "data": {
        "session_id": "uuid-xxx",
        "response": "根据您今天的监测数据分析：\n\n📊 数据概览：\n• 震颤发生次数：12次\n• 平均震颤频率：4.8 Hz（典型帕金森范围）\n...",
        "suggestions": [
            "记录服药时间",
            "查看趋势图",
            "生成报告"
        ]
    }
}
```

### 3.3.7 报告生成接口 (Report API)

#### 生成 PDF 报告 (Generate Report)
```
POST /api/report/generate
Authorization: Bearer <token>

Request Body:
{
    "report_type": "weekly",       // daily/weekly/monthly
    "start_date": "2024-12-11",
    "end_date": "2024-12-18",
    "include_ai_summary": true
}

Response (200 OK):
{
    "success": true,
    "data": {
        "report_id": "uuid-xxx",
        "download_url": "/api/report/download/uuid-xxx",
        "expires_at": "2024-12-19T10:30:00Z"
    }
}
```

---

## 3.4 震颤分析算法 (Tremor Analysis Algorithm)

### 3.4.1 FFT 频谱分析 (FFT Spectrum Analysis)

```python
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq

def analyze_tremor(accel_data: np.ndarray, sample_rate: float = 125.0):
    """
    分析加速度数据中的震颤特征

    Args:
        accel_data: 加速度数据 shape=(N, 3) [x, y, z]
        sample_rate: 采样率 Hz

    Returns:
        dict: 震颤分析结果
    """

    # 1. 计算加速度幅度 (magnitude)
    magnitude = np.sqrt(np.sum(accel_data**2, axis=1))

    # 2. 去除直流分量 (去均值)
    magnitude = magnitude - np.mean(magnitude)

    # 3. 应用带通滤波器 (3-8 Hz, 覆盖帕金森震颤范围)
    nyquist = sample_rate / 2
    low = 3.0 / nyquist
    high = 8.0 / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    filtered = signal.filtfilt(b, a, magnitude)

    # 4. FFT 频谱分析
    n = len(filtered)
    yf = fft(filtered)
    xf = fftfreq(n, 1/sample_rate)

    # 取正频率部分
    positive_freq_idx = xf > 0
    xf = xf[positive_freq_idx]
    yf = np.abs(yf[positive_freq_idx])

    # 5. 在 4-6 Hz 范围内寻找峰值 (帕金森震颤特征频率)
    pd_range = (xf >= 4.0) & (xf <= 6.0)
    if np.any(pd_range):
        pd_freqs = xf[pd_range]
        pd_powers = yf[pd_range]

        # 主频 (最大功率对应的频率)
        dominant_idx = np.argmax(pd_powers)
        dominant_freq = pd_freqs[dominant_idx]
        dominant_power = pd_powers[dominant_idx]

        # 判断是否检测到震颤 (功率阈值)
        tremor_detected = dominant_power > 0.01  # 阈值需要根据实际数据调整
    else:
        dominant_freq = None
        dominant_power = 0
        tremor_detected = False

    # 6. 计算震颤幅度
    if tremor_detected:
        amplitude_mean = np.mean(np.abs(filtered))
        amplitude_max = np.max(np.abs(filtered))
        amplitude_std = np.std(filtered)
    else:
        amplitude_mean = 0
        amplitude_max = 0
        amplitude_std = 0

    # 7. 严重度评估 (简化版，基于幅度)
    severity_score = estimate_severity(amplitude_mean)

    return {
        'tremor_detected': tremor_detected,
        'dominant_frequency': dominant_freq,
        'dominant_power': dominant_power,
        'amplitude_mean': amplitude_mean,
        'amplitude_max': amplitude_max,
        'amplitude_std': amplitude_std,
        'severity_score': severity_score,
        'severity_label': get_severity_label(severity_score)
    }


def estimate_severity(amplitude: float) -> int:
    """
    根据震颤幅度估计严重度 (对应 UPDRS 震颤评分 0-4)

    阈值参考文献: 需要根据临床数据校准
    """
    if amplitude < 0.01:
        return 0  # 无震颤
    elif amplitude < 0.05:
        return 1  # 轻微
    elif amplitude < 0.10:
        return 2  # 轻度
    elif amplitude < 0.20:
        return 3  # 中度
    else:
        return 4  # 重度


def get_severity_label(score: int) -> str:
    labels = {
        0: 'none',
        1: 'slight',
        2: 'mild',
        3: 'moderate',
        4: 'severe'
    }
    return labels.get(score, 'unknown')
```

### 3.4.2 实时震颤检测 (Real-time Detection)

```python
from collections import deque
import numpy as np

class RealtimeTremorDetector:
    """实时震颤检测器"""

    def __init__(self, sample_rate=125, window_seconds=2):
        self.sample_rate = sample_rate
        self.window_size = int(sample_rate * window_seconds)
        self.buffer = deque(maxlen=self.window_size)

    def add_sample(self, accel_x, accel_y, accel_z):
        """添加新的采样点"""
        self.buffer.append([accel_x, accel_y, accel_z])

    def analyze(self):
        """分析当前窗口数据"""
        if len(self.buffer) < self.window_size:
            return None  # 数据不足

        data = np.array(self.buffer)
        return analyze_tremor(data, self.sample_rate)
```

---

## 3.5 数据处理流程 (Data Processing Pipeline)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          数据处理流程                                        │
│                     Data Processing Pipeline                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. 数据接收                                                                │
│   ┌─────────────┐                                                           │
│   │ HTTP/WebSocket │──► 验证设备 Token ──► 解析 JSON ──► 数据验证           │
│   └─────────────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   2. 数据存储                                                                │
│   ┌─────────────┐                                                           │
│   │ 原始数据    │──► PostgreSQL (sensor_data 表)                           │
│   │ 缓存数据    │──► Redis (最近 5 分钟数据，用于实时分析)                   │
│   └─────────────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   3. 实时分析                                                                │
│   ┌─────────────┐                                                           │
│   │ 滑动窗口    │──► FFT 频谱分析 ──► 震颤特征提取 ──► 结果存储             │
│   │ (2秒窗口)   │                                                          │
│   └─────────────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   4. 结果推送                                                                │
│   ┌─────────────┐                                                           │
│   │ WebSocket   │──► 实时数据推送到前端                                     │
│   │ 通道        │                                                          │
│   └─────────────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   5. 定时汇总 (每小时/每天)                                                  │
│   ┌─────────────┐                                                           │
│   │ Cron Job    │──► 聚合统计 ──► 存入 tremor_analysis 表                   │
│   └─────────────┘                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 第四部分：前端网站 (Frontend Website)

## 4.1 技术选型 (Technology Selection)

| 技术 | 版本 | 用途 |
|-----|------|------|
| React | 18.x | UI 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 5.x | 构建工具 |
| Tailwind CSS | 3.x | 样式框架 |
| React Router | 6.x | 路由 |
| TanStack Query | 5.x | 数据请求/缓存 |
| Zustand | 4.x | 状态管理 |
| Chart.js / ECharts | - | 数据可视化 |
| Socket.IO Client | 4.x | WebSocket |
| Axios | 1.x | HTTP 请求 |

---

## 4.2 页面结构 (Page Structure)

```
src/
├── pages/
│   ├── auth/
│   │   ├── Login.tsx           # 登录页
│   │   ├── Register.tsx        # 注册页
│   │   └── ForgotPassword.tsx  # 忘记密码
│   │
│   ├── dashboard/
│   │   └── Dashboard.tsx       # 仪表盘主页
│   │
│   ├── monitor/
│   │   ├── Realtime.tsx        # 实时监测
│   │   └── Waveform.tsx        # 波形图组件
│   │
│   ├── history/
│   │   ├── History.tsx         # 历史数据
│   │   ├── TrendChart.tsx      # 趋势图
│   │   └── EventList.tsx       # 震颤事件列表
│   │
│   ├── ai-doctor/
│   │   ├── AiDoctor.tsx        # AI 医生主页
│   │   ├── ChatWindow.tsx      # 对话窗口
│   │   └── Suggestions.tsx     # 快捷建议
│   │
│   ├── medication/
│   │   ├── Medication.tsx      # 用药管理
│   │   └── Reminder.tsx        # 服药提醒
│   │
│   ├── report/
│   │   ├── Report.tsx          # 报告中心
│   │   └── ReportPreview.tsx   # 报告预览
│   │
│   └── settings/
│       ├── Settings.tsx        # 设置主页
│       ├── Profile.tsx         # 个人信息
│       ├── Device.tsx          # 设备管理
│       └── Notification.tsx    # 通知设置
│
├── components/
│   ├── common/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Footer.tsx
│   │   └── Loading.tsx
│   │
│   ├── charts/
│   │   ├── WaveformChart.tsx   # 实时波形图
│   │   ├── SpectrumChart.tsx   # 频谱图
│   │   ├── TremorTrend.tsx     # 震颤趋势图
│   │   └── SeverityGauge.tsx   # 严重度仪表
│   │
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── Input.tsx
│       └── Modal.tsx
│
├── hooks/
│   ├── useAuth.ts
│   ├── useWebSocket.ts
│   └── useTremorData.ts
│
├── services/
│   ├── api.ts              # API 封装
│   ├── auth.ts             # 认证服务
│   └── websocket.ts        # WebSocket 服务
│
├── stores/
│   ├── authStore.ts
│   └── dataStore.ts
│
└── types/
    ├── user.ts
    ├── device.ts
    ├── sensor.ts
    └── tremor.ts
```

---

## 4.3 页面设计 (Page Design)

### 4.3.1 仪表盘 (Dashboard)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  震颤卫士                                    [用户头像] 张三 ▼              │
├──────────────┬──────────────────────────────────────────────────────────────┤
│              │                                                              │
│  📊 仪表盘   │   今日概览 (2024-12-18)                                      │
│  📈 实时监测 │   ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  📅 历史数据 │   │ 震颤次数   │  │ 平均频率   │  │ 严重程度   │            │
│  🤖 AI医生  │   │     12     │  │  4.8 Hz   │  │   轻度    │            │
│  💊 用药记录 │   │  ↑3 vs昨日 │  │  正常范围  │  │  █████░░░░ │            │
│  📄 报告中心 │   └────────────┘  └────────────┘  └────────────┘            │
│  ⚙️ 设置    │                                                              │
│              │   今日震颤趋势                                               │
│              │   ┌──────────────────────────────────────────────────┐      │
│              │   │     ▲                                            │      │
│              │   │  3 ─┼──────●────────────●──────────              │      │
│              │   │     │     ╱╲            ╱╲                       │      │
│              │   │  2 ─┼────●──●──────────●──●─────                 │      │
│              │   │     │   ╱    ╲        ╱    ╲                     │      │
│              │   │  1 ─┼──●──────●──────●──────●───                 │      │
│              │   │     │ ╱        ╲    ╱        ╲                   │      │
│              │   │  0 ─┼●──────────●──●──────────●─                 │      │
│              │   │     └─────────────────────────────► 时间         │      │
│              │   │      6:00  9:00  12:00 15:00 18:00               │      │
│              │   └──────────────────────────────────────────────────┘      │
│              │                                                              │
│              │   最近震颤事件                                               │
│              │   ┌──────────────────────────────────────────────────┐      │
│              │   │ ● 10:15  持续 3分30秒  频率 4.6Hz  轻度          │      │
│              │   │ ● 14:30  持续 2分15秒  频率 5.2Hz  中度          │      │
│              │   │ ● 16:45  持续 1分45秒  频率 4.4Hz  轻度          │      │
│              │   └──────────────────────────────────────────────────┘      │
│              │                                                              │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

### 4.3.2 实时监测 (Realtime Monitor)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  实时监测                                    ● 已连接  电量: 85%            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   实时波形 (加速度)                                                         │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │ ~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~ X轴   │    │
│   │ ~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~∿∿∿~~~ Y轴   │    │
│   │ ───────────────────────────────────────────────────────── Z轴   │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   实时频谱                              当前状态                            │
│   ┌─────────────────────────────┐      ┌─────────────────────────────┐    │
│   │     ▓                       │      │  震颤检测: ● 检测到          │    │
│   │     ▓▓                      │      │  主频: 4.8 Hz               │    │
│   │   ▓ ▓▓ ▓                    │      │  幅度: 0.12 g               │    │
│   │  ▓▓ ▓▓ ▓▓                   │      │  严重度: 轻度               │    │
│   │  ▓▓ ▓▓ ▓▓ ▓                 │      │                             │    │
│   │ ▓▓▓ ▓▓ ▓▓ ▓▓ ▓              │      │  [开始记录]  [标记事件]     │    │
│   └─────────────────────────────┘      └─────────────────────────────┘    │
│     1  2  3  4  5  6  7  8  Hz                                             │
│           ↑ 帕金森震颤范围 ↑                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3.3 AI 医生 (AI Doctor)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AI 医生                                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐    │
│   │                                                                   │    │
│   │   🤖 AI医生                                        10:30          │    │
│   │   ┌─────────────────────────────────────────────────────────┐   │    │
│   │   │ 您好！我是震颤卫士的AI健康助手。我可以帮您：            │   │    │
│   │   │ • 解读您的震颤监测数据                                  │   │    │
│   │   │ • 回答帕金森相关的健康问题                              │   │    │
│   │   │ • 提供生活方式和康复建议                                │   │    │
│   │   │                                                         │   │    │
│   │   │ 请问有什么可以帮您的？                                  │   │    │
│   │   └─────────────────────────────────────────────────────────┘   │    │
│   │                                                                   │    │
│   │                                        👤 用户         10:32     │    │
│   │                       ┌────────────────────────────────────────┐│    │
│   │                       │ 我今天的震颤数据怎么样？               ││    │
│   │                       └────────────────────────────────────────┘│    │
│   │                                                                   │    │
│   │   🤖 AI医生                                        10:32          │    │
│   │   ┌─────────────────────────────────────────────────────────┐   │    │
│   │   │ 根据您今天的监测数据分析：                              │   │    │
│   │   │                                                         │   │    │
│   │   │ 📊 数据概览：                                           │   │    │
│   │   │ • 震颤发生次数：12次                                    │   │    │
│   │   │ • 平均震颤频率：4.8 Hz（典型帕金森范围）                │   │    │
│   │   │ • 平均持续时间：45秒                                    │   │    │
│   │   │ • 震颤幅度：中等（较昨日略有增加）                      │   │    │
│   │   │                                                         │   │    │
│   │   │ 📈 趋势分析：                                           │   │    │
│   │   │ 与过去7天相比，您今天的震颤频次略高于平均值...          │   │    │
│   │   │                                                         │   │    │
│   │   │ ⚠️ 以上分析仅供参考，不构成医疗诊断。如有疑问，        │   │    │
│   │   │ 请咨询专业医生。                                        │   │    │
│   │   └─────────────────────────────────────────────────────────┘   │    │
│   │                                                                   │    │
│   └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│   快捷提问:                                                                 │
│   [今日数据分析] [用药建议] [康复训练] [什么时候该就医]                    │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────┐ [发送]      │
│   │ 输入您的问题...                                         │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4.4 核心组件实现 (Core Components)

### 4.4.1 实时波形图组件 (WaveformChart.tsx)

```typescript
// src/components/charts/WaveformChart.tsx

import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

interface WaveformProps {
  data: {
    x: number[];
    y: number[];
    z: number[];
  };
  maxPoints?: number;
}

export const WaveformChart: React.FC<WaveformProps> = ({
  data,
  maxPoints = 500
}) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    const ctx = chartRef.current.getContext('2d');
    if (!ctx) return;

    // 创建图表
    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels: Array.from({ length: maxPoints }, (_, i) => i),
        datasets: [
          {
            label: 'X轴',
            data: data.x,
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1,
            pointRadius: 0,
            tension: 0.1
          },
          {
            label: 'Y轴',
            data: data.y,
            borderColor: 'rgb(54, 162, 235)',
            borderWidth: 1,
            pointRadius: 0,
            tension: 0.1
          },
          {
            label: 'Z轴',
            data: data.z,
            borderColor: 'rgb(75, 192, 192)',
            borderWidth: 1,
            pointRadius: 0,
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        animation: false,
        scales: {
          x: { display: false },
          y: {
            min: -2,
            max: 2,
            title: { display: true, text: '加速度 (g)' }
          }
        },
        plugins: {
          legend: { position: 'top' }
        }
      }
    });

    return () => {
      chartInstance.current?.destroy();
    };
  }, []);

  // 更新数据
  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.data.datasets[0].data = data.x;
      chartInstance.current.data.datasets[1].data = data.y;
      chartInstance.current.data.datasets[2].data = data.z;
      chartInstance.current.update('none');
    }
  }, [data]);

  return (
    <div className="w-full h-64">
      <canvas ref={chartRef}></canvas>
    </div>
  );
};
```

### 4.4.2 WebSocket Hook (useWebSocket.ts)

```typescript
// src/hooks/useWebSocket.ts

import { useEffect, useRef, useState, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAuthStore } from '../stores/authStore';

interface SensorData {
  timestamp: string;
  accel: { x: number; y: number; z: number };
  gyro: { x: number; y: number; z: number };
  tremor?: {
    detected: boolean;
    frequency: number;
    amplitude: number;
  };
}

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [sensorData, setSensorData] = useState<SensorData | null>(null);
  const socketRef = useRef<Socket | null>(null);
  const { token } = useAuthStore();

  const connect = useCallback(() => {
    if (!token) return;

    socketRef.current = io(import.meta.env.VITE_WS_URL, {
      auth: { token },
      transports: ['websocket']
    });

    socketRef.current.on('connect', () => {
      setIsConnected(true);
      console.log('WebSocket 已连接');
    });

    socketRef.current.on('disconnect', () => {
      setIsConnected(false);
      console.log('WebSocket 已断开');
    });

    socketRef.current.on('sensor_data', (data: SensorData) => {
      setSensorData(data);
    });

    socketRef.current.on('error', (error) => {
      console.error('WebSocket 错误:', error);
    });
  }, [token]);

  const disconnect = useCallback(() => {
    socketRef.current?.disconnect();
    socketRef.current = null;
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    sensorData,
    connect,
    disconnect
  };
};
```

---

# 第五部分：AI 医生模块 (AI Doctor Module)

## 5.1 技术架构 (Technical Architecture)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI 医生模块架构                                      │
│                      AI Doctor Module Architecture                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   用户输入                                                                   │
│   ┌─────────────┐                                                           │
│   │ "我今天的   │                                                           │
│   │ 震颤数据    │                                                           │
│   │ 怎么样？"   │                                                           │
│   └──────┬──────┘                                                           │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Prompt 构建层                                 │      │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │      │
│   │  │ System       │  │ 用户数据     │  │ RAG 检索     │          │      │
│   │  │ Prompt       │  │ Context      │  │ 结果         │          │      │
│   │  │ (角色定义)   │  │ (震颤历史)   │  │ (知识库)     │          │      │
│   │  └──────────────┘  └──────────────┘  └──────────────┘          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                    Claude API                                    │      │
│   │                 (claude-3-sonnet-20240229)                      │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                   安全过滤层                                     │      │
│   │  • 敏感词过滤  • 医疗安全检查  • 免责声明添加                   │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────┐                                                           │
│   │ AI 回复     │                                                           │
│   └─────────────┘                                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5.2 System Prompt 设计 (System Prompt Design)

```python
# ai_doctor/prompts.py

SYSTEM_PROMPT = """
你是"震颤卫士"的AI健康助手，专注于帕金森病相关的健康咨询服务。

## 你的身份
- 名称：震颤卫士AI助手
- 定位：健康咨询助手（非医生）
- 专长：帕金森病知识、震颤数据解读、生活方式指导

## 你的职责
1. **数据解读**：分析用户的震颤监测数据，用通俗易懂的语言解释各项指标的含义
2. **健康问答**：回答帕金森病相关的健康问题，包括症状、用药、康复等
3. **生活建议**：提供日常生活、饮食、运动等方面的建议
4. **就医提醒**：在必要时提醒用户及时就医

## 重要原则（必须严格遵守）

### 医疗安全边界
1. **禁止诊断**：你不是医生，不能对疾病进行诊断。避免使用"您患有..."、"这是..."等诊断性表述
2. **禁止处方**：不能推荐具体药物名称或剂量。如用户询问药物，建议咨询医生
3. **免责提示**：每次回复结尾都要加上："⚠️ 以上建议仅供参考，不构成医疗诊断。如有疑问，请咨询专业医生。"

### 紧急情况处理
如果用户描述以下情况，立即建议就医：
- 突然无法行动或严重肢体僵硬
- 跌倒或有跌倒风险
- 严重的药物副作用（如幻觉、精神症状）
- 吞咽困难或呼吸困难
- 高热或感染症状
- 情绪极度低落或有自伤倾向

### 沟通风格
- 语言：温和、耐心、专业
- 格式：使用 emoji 增加亲和力，使用列表增强可读性
- 态度：尊重用户，不评判用户的行为或决定

## 帕金森病基础知识

### 典型震颤特征
- 静止性震颤：休息时明显，运动时减轻
- 频率：4-6 Hz（每秒4-6次）
- 特点：单侧起病，逐渐发展为双侧

### 震颤严重度参考 (UPDRS 标准)
- 0级：无震颤
- 1级：轻微，仅偶尔出现
- 2级：轻度，幅度小于2cm
- 3级：中度，幅度2-4cm
- 4级：重度，幅度大于4cm

### 药物知识（仅供参考，不推荐具体用药）
- 左旋多巴：帕金森病一线用药，需注意"开关现象"
- 多巴胺受体激动剂：如普拉克索，可能引起嗜睡
- MAO-B抑制剂：如雷沙吉兰，有神经保护作用

## 用户数据上下文
{user_context}
"""

# 用户上下文模板
USER_CONTEXT_TEMPLATE = """
### 用户基本信息
- 用户名：{username}
- 确诊时间：{diagnosis_date}
- 病情阶段：{disease_stage}

### 今日震颤数据摘要
- 震颤次数：{tremor_count} 次
- 平均频率：{avg_frequency} Hz
- 平均持续时间：{avg_duration} 秒
- 最大幅度：{max_amplitude}
- 严重度分布：轻度 {mild_count} 次，中度 {moderate_count} 次，重度 {severe_count} 次

### 过去7天趋势
- 日均震颤次数：{weekly_avg_count}
- 震颤频次变化：{trend_direction}（较上周{trend_percentage}）

### 用药记录（今日）
{medication_records}
"""
```

---

## 5.3 RAG 知识库 (RAG Knowledge Base)

### 5.3.1 知识库结构

```
knowledge_base/
├── parkinson_basics/
│   ├── symptoms.md           # 症状介绍
│   ├── stages.md             # 病程分期
│   └── diagnosis.md          # 诊断标准
│
├── medication_guide/
│   ├── levodopa.md           # 左旋多巴
│   ├── dopamine_agonists.md  # 多巴胺受体激动剂
│   ├── mao_inhibitors.md     # MAO-B抑制剂
│   └── side_effects.md       # 常见副作用
│
├── rehabilitation/
│   ├── exercise.md           # 运动康复
│   ├── speech_therapy.md     # 言语治疗
│   └── daily_activities.md   # 日常活动训练
│
├── lifestyle/
│   ├── diet.md               # 饮食建议
│   ├── sleep.md              # 睡眠管理
│   └── mental_health.md      # 心理健康
│
└── faq/
    ├── common_questions.md   # 常见问题
    └── emergency.md          # 紧急情况
```

### 5.3.2 RAG 实现代码

```python
# ai_doctor/rag.py

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
import os

class TremorGuardRAG:
    """震颤卫士 RAG 知识库"""

    def __init__(self, knowledge_path: str = "./knowledge_base"):
        self.knowledge_path = knowledge_path
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def load_knowledge_base(self):
        """加载知识库文档"""
        # 加载所有 Markdown 文件
        loader = DirectoryLoader(
            self.knowledge_path,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()

        # 文本分割
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "，", " "]
        )
        splits = text_splitter.split_documents(documents)

        # 创建向量存储
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )

        print(f"知识库已加载，共 {len(splits)} 个文档片段")

    def retrieve(self, query: str, k: int = 3) -> list:
        """检索相关文档"""
        if not self.vector_store:
            raise ValueError("知识库未加载，请先调用 load_knowledge_base()")

        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def get_context(self, query: str) -> str:
        """获取 RAG 上下文"""
        docs = self.retrieve(query)
        context = "\n\n---\n\n".join(docs)
        return f"### 相关知识参考\n\n{context}"
```

---

## 5.4 AI 对话服务 (AI Chat Service)

```python
# ai_doctor/chat_service.py

import anthropic
from typing import Optional, List, Dict
from .prompts import SYSTEM_PROMPT, USER_CONTEXT_TEMPLATE
from .rag import TremorGuardRAG

class AIDoctorService:
    """AI 医生对话服务"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.rag = TremorGuardRAG()
        self.rag.load_knowledge_base()

    async def chat(
        self,
        user_message: str,
        user_id: str,
        session_id: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """
        AI 对话

        Args:
            user_message: 用户消息
            user_id: 用户 ID
            session_id: 会话 ID
            conversation_history: 对话历史

        Returns:
            AI 回复
        """

        # 1. 获取用户数据上下文
        user_context = await self._get_user_context(user_id)

        # 2. RAG 检索相关知识
        rag_context = self.rag.get_context(user_message)

        # 3. 构建完整的 System Prompt
        system_prompt = SYSTEM_PROMPT.format(
            user_context=user_context + "\n\n" + rag_context
        )

        # 4. 构建消息列表
        messages = []

        # 添加对话历史
        if conversation_history:
            for msg in conversation_history[-10:]:  # 只保留最近10条
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": user_message
        })

        # 5. 调用 Claude API
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        ai_response = response.content[0].text

        # 6. 安全过滤
        ai_response = self._apply_safety_filter(ai_response)

        # 7. 添加免责声明（如果没有）
        if "⚠️" not in ai_response and "仅供参考" not in ai_response:
            ai_response += "\n\n⚠️ 以上建议仅供参考，不构成医疗诊断。如有疑问，请咨询专业医生。"

        return ai_response

    async def _get_user_context(self, user_id: str) -> str:
        """获取用户数据上下文"""
        # 从数据库获取用户数据
        # 这里是示例实现，实际需要查询数据库

        user_data = await self._fetch_user_data(user_id)
        tremor_summary = await self._fetch_tremor_summary(user_id)
        medication_records = await self._fetch_medication_records(user_id)

        return USER_CONTEXT_TEMPLATE.format(
            username=user_data.get("username", "用户"),
            diagnosis_date=user_data.get("diagnosis_date", "未知"),
            disease_stage=user_data.get("disease_stage", "未知"),
            tremor_count=tremor_summary.get("count", 0),
            avg_frequency=tremor_summary.get("avg_frequency", 0),
            avg_duration=tremor_summary.get("avg_duration", 0),
            max_amplitude=tremor_summary.get("max_amplitude", 0),
            mild_count=tremor_summary.get("mild_count", 0),
            moderate_count=tremor_summary.get("moderate_count", 0),
            severe_count=tremor_summary.get("severe_count", 0),
            weekly_avg_count=tremor_summary.get("weekly_avg", 0),
            trend_direction=tremor_summary.get("trend", "持平"),
            trend_percentage=tremor_summary.get("trend_pct", "0%"),
            medication_records=medication_records
        )

    def _apply_safety_filter(self, text: str) -> str:
        """安全过滤"""
        # 过滤可能的诊断性表述
        dangerous_patterns = [
            ("您患有", "您可能存在"),
            ("这是", "这可能是"),
            ("确诊为", "疑似"),
            ("建议服用", "可以咨询医生关于"),
            ("剂量调整为", "剂量调整需要咨询医生")
        ]

        for old, new in dangerous_patterns:
            text = text.replace(old, new)

        return text

    # 数据库查询方法（示例）
    async def _fetch_user_data(self, user_id: str) -> dict:
        # TODO: 实现数据库查询
        return {}

    async def _fetch_tremor_summary(self, user_id: str) -> dict:
        # TODO: 实现数据库查询
        return {}

    async def _fetch_medication_records(self, user_id: str) -> str:
        # TODO: 实现数据库查询
        return "暂无用药记录"
```

---

## 5.5 安全边界设计 (Safety Boundaries)

### 5.5.1 医疗安全规则

| 规则 | 实现方式 | 示例 |
|-----|---------|------|
| 禁止诊断 | System Prompt + 过滤器 | "您患有"→"您可能存在" |
| 禁止处方 | System Prompt + 关键词检测 | 不提及具体药物剂量 |
| 免责声明 | 自动添加 | 每次回复末尾添加 |
| 紧急转介 | 关键词触发 | 检测到"跌倒"等词，提示就医 |

### 5.5.2 紧急情况检测

```python
# ai_doctor/safety.py

EMERGENCY_KEYWORDS = [
    # 跌倒相关
    "跌倒", "摔倒", "摔跤", "站不稳",
    # 药物反应
    "幻觉", "看到不存在的", "精神恍惚",
    # 生命体征
    "无法呼吸", "呼吸困难", "胸闷", "高烧",
    # 心理危机
    "不想活", "自杀", "自残", "活着没意思",
    # 严重症状
    "完全无法动", "全身僵硬", "吞不下去"
]

def check_emergency(text: str) -> tuple[bool, str]:
    """
    检测是否为紧急情况

    Returns:
        (is_emergency, emergency_type)
    """
    text_lower = text.lower()

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text_lower:
            return True, keyword

    return False, ""

EMERGENCY_RESPONSE = """
⚠️ **紧急提醒**

您描述的情况可能需要立即就医。请：

1. **保持冷静**，确保自身安全
2. **立即联系家人或照护者**
3. **拨打急救电话 120** 或前往最近医院急诊

如果情况危急，请立即拨打 **120**。

---
您的安全是最重要的。以上不是医疗诊断，请务必寻求专业医疗帮助。
"""
```

---

# 第六部分：数据流设计 (Data Flow Design)

## 6.1 完整数据流图 (Complete Data Flow)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              完整数据流图                                    │
│                         Complete Data Flow Diagram                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              ┌─────────────┐                                │
│                              │   用户手环   │                                │
│                              │  ESP32-C3   │                                │
│                              │  + MPU6050  │                                │
│                              └──────┬──────┘                                │
│                                     │                                       │
│                          ① WiFi HTTP POST                                  │
│                          (每秒上传 ~125 个采样点)                           │
│                                     │                                       │
│                                     ▼                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                            后端服务器                                 │  │
│   │                          Backend Server                              │  │
│   │  ┌─────────────────────────────────────────────────────────────┐   │  │
│   │  │                      API Gateway                              │   │  │
│   │  │  • 认证验证 (JWT)                                            │   │  │
│   │  │  • 请求限流 (Rate Limiting)                                  │   │  │
│   │  │  • 数据验证 (Schema Validation)                              │   │  │
│   │  └─────────────────────────┬───────────────────────────────────┘   │  │
│   │                            │                                        │  │
│   │              ┌─────────────┼─────────────┐                         │  │
│   │              │             │             │                         │  │
│   │              ▼             ▼             ▼                         │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │  │
│   │  │ ② 数据存储  │  │ ③ 实时分析  │  │ ④ 消息推送  │                │  │
│   │  │ PostgreSQL  │  │   FFT 频谱  │  │  WebSocket  │                │  │
│   │  │ + Redis     │  │   震颤检测  │  │   Channel   │                │  │
│   │  └─────────────┘  └──────┬──────┘  └──────┬──────┘                │  │
│   │                          │                │                        │  │
│   │                          └────────┬───────┘                        │  │
│   │                                   │                                │  │
│   │                                   ▼                                │  │
│   │                          ┌─────────────┐                          │  │
│   │                          │ ⑤ AI 医生   │                          │  │
│   │                          │ Claude API  │                          │  │
│   │                          │ + RAG       │                          │  │
│   │                          └─────────────┘                          │  │
│   │                                                                    │  │
│   └────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│                          ⑥ WebSocket / HTTP                                │
│                                     │                                       │
│                                     ▼                                       │
│                              ┌─────────────┐                                │
│                              │   前端网站   │                                │
│                              │ React + TS  │                                │
│                              │  用户界面   │                                │
│                              └─────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 6.2 数据流详细说明

| 步骤 | 数据流向 | 协议/格式 | 频率 | 说明 |
|-----|---------|----------|------|------|
| ① | 手环 → 后端 | HTTP POST / JSON | 1次/秒 | 每批次约 125 个采样点 |
| ② | 后端 → 数据库 | SQL / Redis Protocol | 实时 | 原始数据存 PostgreSQL，最近数据存 Redis |
| ③ | Redis → 分析模块 | 内存读取 | 2秒/次 | 滑动窗口 FFT 分析 |
| ④ | 分析结果 → WebSocket | WebSocket / JSON | 实时 | 推送震颤检测结果到前端 |
| ⑤ | 用户对话 → AI | Claude API | 按需 | 用户发起对话时调用 |
| ⑥ | 后端 → 前端 | HTTP + WebSocket | 实时 | 数据展示和交互 |

---

# 第七部分：开发任务清单 (Development Checklist)

## 7.1 硬件开发任务 (Hardware Tasks)

### Phase 1: 基础功能 (已完成)
- [x] MPU6050 I2C 通信初始化
- [x] 传感器配置 (加速度计 ±2g, 陀螺仪 ±250°/s)
- [x] 数据读取功能
- [x] 串口命令系统

### Phase 2: 网络功能
- [ ] WiFi 连接管理
  - [ ] WiFi 配置存储 (EEPROM/NVS)
  - [ ] 自动重连机制
  - [ ] 配网功能 (SmartConfig / BLE配网)
- [ ] HTTP 数据上传
  - [ ] JSON 数据封装
  - [ ] 批量上传 (每秒一次)
  - [ ] 失败重试机制
  - [ ] 离线数据缓存

### Phase 3: 电源管理
- [ ] 电池电量监测 (ADC)
- [ ] 低功耗模式
  - [ ] Deep Sleep 实现
  - [ ] 运动唤醒 (MPU6050 Motion Detection)
- [ ] 充电检测

### Phase 4: 产品化
- [ ] 固件 OTA 升级
- [ ] LED 状态指示
- [ ] 按键功能

---

## 7.2 后端开发任务 (Backend Tasks)

### Phase 1: 项目搭建
- [ ] 项目初始化 (FastAPI / Express)
- [ ] 数据库设计和迁移
- [ ] 用户认证系统 (JWT)
- [ ] API 文档 (Swagger / OpenAPI)

### Phase 2: 核心 API
- [ ] 用户 API
  - [ ] 注册 / 登录 / 登出
  - [ ] 个人信息管理
- [ ] 设备 API
  - [ ] 设备绑定 / 解绑
  - [ ] 设备状态查询
- [ ] 数据 API
  - [ ] 数据上传接口
  - [ ] 历史数据查询
  - [ ] WebSocket 实时数据

### Phase 3: 震颤分析
- [ ] FFT 频谱分析算法
- [ ] 震颤特征提取
- [ ] 严重度评估算法
- [ ] 定时汇总任务 (Cron Job)

### Phase 4: AI 集成
- [ ] Claude API 集成
- [ ] RAG 知识库构建
- [ ] AI 对话 API
- [ ] 安全过滤器

### Phase 5: 报告功能
- [ ] PDF 报告生成
- [ ] 报告模板设计
- [ ] 报告下载 API

---

## 7.3 前端开发任务 (Frontend Tasks)

### Phase 1: 项目搭建
- [ ] React + TypeScript + Vite 初始化
- [ ] Tailwind CSS 配置
- [ ] 路由配置
- [ ] API 服务封装
- [ ] 状态管理 (Zustand)

### Phase 2: 认证模块
- [ ] 登录页面
- [ ] 注册页面
- [ ] Token 管理
- [ ] 路由守卫

### Phase 3: 核心页面
- [ ] 仪表盘 Dashboard
  - [ ] 今日概览卡片
  - [ ] 震颤趋势图
  - [ ] 最近事件列表
- [ ] 实时监测页
  - [ ] 实时波形图
  - [ ] 频谱分析图
  - [ ] 状态指示器
  - [ ] WebSocket 集成
- [ ] 历史数据页
  - [ ] 日期范围选择
  - [ ] 趋势图表
  - [ ] 事件详情
- [ ] AI 医生页
  - [ ] 对话界面
  - [ ] 消息列表
  - [ ] 快捷提问
  - [ ] 历史记录

### Phase 4: 辅助页面
- [ ] 用药管理
- [ ] 报告中心
- [ ] 设置页面
- [ ] 设备管理

### Phase 5: 优化
- [ ] 响应式设计
- [ ] 加载状态
- [ ] 错误处理
- [ ] 性能优化

---

## 7.4 AI 开发任务 (AI Tasks)

### Phase 1: 基础对话
- [ ] Claude API 集成
- [ ] System Prompt 设计
- [ ] 基础对话功能
- [ ] 会话管理

### Phase 2: 知识增强
- [ ] RAG 知识库搭建
- [ ] 知识文档编写
  - [ ] 帕金森病基础知识
  - [ ] 用药指南
  - [ ] 康复训练
  - [ ] 常见问题
- [ ] 向量数据库集成

### Phase 3: 数据集成
- [ ] 用户数据上下文注入
- [ ] 震颤数据解读
- [ ] 个性化建议生成

### Phase 4: 安全优化
- [ ] 安全过滤器
- [ ] 紧急情况检测
- [ ] 免责声明
- [ ] 测试和验证

---

## 7.5 集成测试任务 (Integration Tasks)

### 系统集成
- [ ] 硬件 ↔ 后端 数据上传测试
- [ ] 后端 ↔ 前端 API 联调
- [ ] WebSocket 实时通信测试
- [ ] AI 对话功能测试

### 端到端测试
- [ ] 完整数据流测试
- [ ] 用户场景测试
- [ ] 异常情况处理测试
- [ ] 性能压力测试

### 部署
- [ ] 后端部署 (云服务器)
- [ ] 数据库部署
- [ ] 前端部署 (CDN)
- [ ] 域名和 HTTPS 配置

---

# 附录 (Appendix)

## A. 参考资料 (References)

### 技术文档
- [ESP32-C3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [MPU6050 Register Map](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Claude API Documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)

### 医学参考
- 《中国帕金森病治疗指南 (第四版)》- 中华医学会神经病学分会
- Movement Disorders Society - UPDRS 评估标准

---

## B. 环境配置 (Environment Setup)

### 硬件开发环境
```bash
# Arduino IDE 配置
# 1. 添加 ESP32 开发板支持
# 文件 -> 首选项 -> 附加开发板管理器网址
# https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

# 2. 安装 ESP32 开发板
# 工具 -> 开发板 -> 开发板管理器 -> 搜索 "esp32" -> 安装

# 3. 选择开发板
# 工具 -> 开发板 -> ESP32 Arduino -> XIAO_ESP32C3
```

### 后端开发环境 (Python)
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install fastapi uvicorn sqlalchemy asyncpg redis
pip install numpy scipy pandas
pip install anthropic langchain chromadb
pip install python-jose[cryptography] passlib[bcrypt]

# 运行开发服务器
uvicorn main:app --reload --port 8000
```

### 前端开发环境
```bash
# 创建项目
npm create vite@latest tremor-guard-web -- --template react-ts

# 安装依赖
cd tremor-guard-web
npm install
npm install -D tailwindcss postcss autoprefixer
npm install @tanstack/react-query zustand axios socket.io-client
npm install chart.js react-chartjs-2
npm install react-router-dom

# 初始化 Tailwind
npx tailwindcss init -p

# 运行开发服务器
npm run dev
```

---

## C. 常见问题 (FAQ)

### Q1: MPU6050 无法识别怎么办？
**A**: 请检查：
1. I2C 接线是否正确 (SDA→GPIO6, SCL→GPIO7)
2. 是否添加了 4.7kΩ 上拉电阻
3. 电源电压是否为 3.3V
4. 使用 `scan` 命令扫描 I2C 总线

### Q2: 震颤检测不准确怎么优化？
**A**:
1. 确保采样率足够 (推荐 125Hz)
2. 调整 FFT 窗口大小 (推荐 2-4 秒)
3. 调整震颤检测阈值
4. 增加训练数据，优化算法

### Q3: AI 医生回复不专业怎么办？
**A**:
1. 优化 System Prompt，增加医学知识
2. 扩充 RAG 知识库
3. 调整 Temperature 参数
4. 增加安全过滤规则

---

**文档结束 / End of Document**

*最后更新: 2024年12月*
*版本: 1.0*
