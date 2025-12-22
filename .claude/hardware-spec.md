# Tremor Guard 硬件系统技术规格

帕金森震颤监测手环 (Tremor Guard) 硬件系统完整技术文档

---

## 目录

1. [系统概述](#1-系统概述)
2. [硬件架构](#2-硬件架构)
3. [引脚配置](#3-引脚配置)
4. [MPU6050 配置](#4-mpu6050-配置)
5. [固件模块](#5-固件模块)
6. [震颤检测算法](#6-震颤检测算法)
7. [网络通信协议](#7-网络通信协议)
8. [配置系统](#8-配置系统)
9. [串口命令](#9-串口命令)
10. [数据流与时序](#10-数据流与时序)

---

## 1. 系统概述

### 1.1 项目目标

通过 FFT 频谱分析检测 4-6Hz 帕金森特征震颤，实时评估严重度等级 (0-4 级)，并将数据上传至云端进行分析和存储。

### 1.2 核心功能

- **震颤检测**: 基于 FFT 的 4-6Hz 帕金森震颤识别
- **严重度评估**: 根据 RMS 幅度自动分级 (无/轻微/轻度/中度/重度)
- **云端同步**: 实时数据上传 + 配置远程管理
- **离线缓存**: 断网时本地缓存，恢复后自动上传

### 1.3 版本信息

```
固件版本: 1.1.0
协议版本: HTTP/HTTPS
最后更新: 2024
```

---

## 2. 硬件架构

### 2.1 核心组件

| 组件 | 型号 | 功能 |
|------|------|------|
| MCU | Seeed XIAO ESP32-C3 | 主控制器 (WiFi/BLE) |
| 传感器 | MPU6050 | 6轴惯性测量单元 |
| 接口 | USB-C | 供电 + 串口调试 |

### 2.2 ESP32-C3 规格

- **核心**: RISC-V 单核 160MHz
- **内存**: 400KB SRAM, 4MB Flash
- **无线**: WiFi 802.11 b/g/n + BLE 5.0
- **GPIO**: 11 个可用引脚
- **ADC**: 2 通道 12-bit
- **I2C/SPI/UART**: 各 1 个

### 2.3 MPU6050 规格

- **类型**: MEMS 6轴惯性传感器
- **加速度计**: ±2g/±4g/±8g/±16g 可选
- **陀螺仪**: ±250/±500/±1000/±2000 °/s 可选
- **接口**: I2C (最高 400kHz)
- **采样率**: 最高 1kHz
- **内置**: 数字低通滤波器 (DLPF)

### 2.4 供电要求

| 参数 | 值 |
|------|-----|
| 工作电压 | 3.3V |
| 典型电流 | ~50mA (WiFi 活动) |
| 睡眠电流 | ~20μA |
| 供电方式 | USB-C 或锂电池 |

---

## 3. 引脚配置

### 3.1 I2C 总线

```
XIAO ESP32-C3          MPU6050
─────────────          ───────
GPIO6 (D4/SDA) ──────► SDA
GPIO7 (D5/SCL) ──────► SCL
3V3            ──────► VDD, VLOGIC
GND            ──────► GND
GPIO5 (D3)     ──────► INT (可选)
```

### 3.2 引脚定义 (代码)

```cpp
// mpu6050_init.ino
#define I2C_SDA_PIN     6       // GPIO6 → SDA
#define I2C_SCL_PIN     7       // GPIO7 → SCL
#define MPU6050_INT_PIN 5       // GPIO5 → INT (可选)
#define I2C_CLOCK_SPEED 100000  // 100kHz 标准模式
```

### 3.3 I2C 地址

| 地址 | 条件 |
|------|------|
| 0x68 | AD0 引脚接 GND (默认) |
| 0x69 | AD0 引脚接 VCC |

### 3.4 硬件连接注意事项

1. **上拉电阻**: I2C 总线需要 4.7kΩ 上拉电阻 (SDA, SCL 各一个)
2. **电平匹配**: ESP32-C3 和 MPU6050 都是 3.3V 逻辑电平
3. **去耦电容**: MPU6050 VDD 旁需加 100nF 去耦电容
4. **线长限制**: I2C 走线应尽量短 (< 30cm)

---

## 4. MPU6050 配置

### 4.1 寄存器映射

| 寄存器名 | 地址 | 功能 | 配置值 |
|---------|------|------|--------|
| PWR_MGMT_1 | 0x6B | 电源管理 | 0x01 (PLL X轴陀螺仪) |
| SMPLRT_DIV | 0x19 | 采样率分频 | 0x07 (125Hz) |
| CONFIG | 0x1A | DLPF 配置 | 0x03 (44Hz 带宽) |
| GYRO_CONFIG | 0x1B | 陀螺仪量程 | 0x00 (±250°/s) |
| ACCEL_CONFIG | 0x1C | 加速度计量程 | 0x00 (±2g) |
| WHO_AM_I | 0x75 | 芯片 ID | 0x68 (只读) |

### 4.2 数据寄存器

| 数据类型 | 起始地址 | 字节数 | 格式 |
|---------|---------|--------|------|
| 加速度 X | 0x3B | 2 | int16, 大端 |
| 加速度 Y | 0x3D | 2 | int16, 大端 |
| 加速度 Z | 0x3F | 2 | int16, 大端 |
| 温度 | 0x41 | 2 | int16, 大端 |
| 陀螺仪 X | 0x43 | 2 | int16, 大端 |
| 陀螺仪 Y | 0x45 | 2 | int16, 大端 |
| 陀螺仪 Z | 0x47 | 2 | int16, 大端 |

### 4.3 灵敏度系数

| 量程 | 灵敏度 | 分辨率 |
|------|--------|--------|
| ±2g | 16384 LSB/g | 0.06 mg/LSB |
| ±250°/s | 131 LSB/(°/s) | 0.0076 °/s/LSB |

### 4.4 采样率计算

```
采样率 = 陀螺仪输出率 / (1 + SMPLRT_DIV)
       = 1000Hz / (1 + 7)
       = 125Hz

采样周期 = 1 / 125Hz = 8ms
```

### 4.5 温度计算

```cpp
温度(°C) = TEMP_OUT / 340.0 + 36.53
```

---

## 5. 固件模块

### 5.1 文件结构

```
mpu6050_init/
├── mpu6050_init.ino        # 主程序 (初始化、命令处理、主循环)
├── tremor_detection.h      # 震颤检测接口
├── tremor_detection.cpp    # FFT 算法实现
├── tremor_config.h         # 检测参数配置
├── network_config.h        # 网络参数配置
├── wifi_manager.h          # WiFi 管理接口
├── wifi_manager.cpp        # WiFi 实现
├── http_client.h           # HTTP 客户端接口
├── http_client.cpp         # HTTP/HTTPS 实现
├── data_uploader.h         # 数据上传接口
├── data_uploader.cpp       # 批量上传实现
├── config_sync.h           # 配置同步接口
└── config_sync.cpp         # 云端配置同步
```

### 5.2 模块功能

| 模块 | 职责 |
|------|------|
| **mpu6050_init.ino** | 硬件初始化、I2C 通信、传感器读取、命令处理 |
| **tremor_detection** | FFT 分析、频谱计算、震颤检测、严重度评估 |
| **tremor_config** | 检测阈值、FFT 参数、运行时配置结构 |
| **network_config** | 服务器地址、API 路径、超时参数 |
| **wifi_manager** | WiFi 连接、断开、重连、状态监控 |
| **http_client** | HTTPS 请求、JSON 序列化、错误处理 |
| **data_uploader** | 批量缓存、离线存储、自动上传 |
| **config_sync** | 云端配置拉取、本地配置推送 |

### 5.3 依赖库

```cpp
#include <Wire.h>           // I2C 通信
#include <WiFi.h>           // ESP32 WiFi
#include <HTTPClient.h>     // HTTP 客户端
#include <WiFiClientSecure.h> // HTTPS 支持
#include <ArduinoJson.h>    // JSON 处理
#include <arduinoFFT.h>     // FFT 库
```

---

## 6. 震颤检测算法

### 6.1 FFT 参数

| 参数 | 值 | 说明 |
|------|-----|------|
| FFT_SAMPLES | 256 | 采样点数 (2的幂) |
| SAMPLE_RATE | 125 Hz | 采样频率 |
| 采集时间 | ~2048 ms | 256 × 8ms |
| 频率分辨率 | 0.488 Hz | 125/256 |

### 6.2 帕金森震颤频率

```
目标频率范围: 4.0 - 6.0 Hz
对应 FFT bin: 8 - 12
```

### 6.3 检测阈值 (可运行时修改)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| TREMOR_RMS_MIN | 2.5 g | RMS 幅度下限 |
| TREMOR_RMS_MAX | 5.0 g | RMS 幅度上限 (超出则无效) |
| TREMOR_POWER_THRESHOLD | 0.5 | 频段功率阈值 |
| TREMOR_FREQ_MIN | 4.0 Hz | 频率下限 |
| TREMOR_FREQ_MAX | 6.0 Hz | 频率上限 |

### 6.4 严重度分级

| 等级 | 标签 | RMS 范围 | 颜色 |
|------|------|---------|------|
| 0 | 无 (None) | < 2.5g | 灰色 |
| 1 | 轻微 (Slight) | 2.5 - 3.0g | 黄色 |
| 2 | 轻度 (Mild) | 3.0 - 3.5g | 橙色 |
| 3 | 中度 (Moderate) | 3.5 - 4.0g | 红色 |
| 4 | 重度 (Severe) | > 4.0g | 深红 |

### 6.5 算法流程

```
1. 数据采集 (collectSamples)
   └─ 读取 256 个加速度样本
   └─ 计算向量幅度: magnitude = √(ax² + ay² + az²)
   └─ 存入 vReal[] 数组

2. 预处理 (removeDC)
   └─ 计算平均值 (DC 分量)
   └─ 减去平均值实现去直流

3. 加窗 (Hamming Window)
   └─ FFT.Windowing(HAMMING, FFT_FORWARD)
   └─ 减少频谱泄漏

4. FFT 变换 (performFFTAnalysis)
   └─ FFT.Compute(FORWARD)
   └─ FFT.ComplexToMagnitude()

5. 频谱分析 (analyzeSpectrum)
   └─ 计算 4-6Hz 频段功率
   └─ 寻找峰值频率
   └─ 检测震颤条件

6. 结果评估 (tremorAnalyze)
   └─ 检查 RMS 范围
   └─ 计算严重度等级
   └─ 生成 TremorResult
```

### 6.6 检测条件

```
震颤判定 = (频段功率 > 阈值) AND
           (峰值频率 在 4-6Hz 内) AND
           (RMS 幅度 在有效范围内)
```

---

## 7. 网络通信协议

### 7.1 服务器配置

```cpp
// network_config.h
#define SERVER_HOST         "parkinson.zeabur.app"
#define SERVER_PORT         443
#define SERVER_USE_HTTPS    true
#define DEVICE_ID           "TG-ESP32-001"
```

### 7.2 API 接口

| 端点 | 方法 | 功能 | 请求体 |
|------|------|------|--------|
| `/api/test/receive` | POST | 单条数据上传 | TremorResult JSON |
| `/api/test/batch` | POST | 批量数据上传 | TremorResult[] |
| `/api/test/heartbeat` | POST | 心跳检测 | {device_id, timestamp} |
| `/api/config/current` | GET | 获取云端配置 | 无 |
| `/api/config/upload` | POST | 上传设备配置 | TremorConfig JSON |

### 7.3 数据格式

**震颤结果 (TremorResult):**
```json
{
  "deviceId": "TG-ESP32-001",
  "timestamp": 1703001234,
  "detected": true,
  "frequency": 4.8,
  "rmsAmplitude": 3.2,
  "severity": 2,
  "severityLabel": "轻度",
  "bandPower": 0.75,
  "valid": true,
  "outOfRange": false
}
```

**配置数据 (TremorConfig):**
```json
{
  "device_id": "TG-ESP32-001",
  "config_version": 1,
  "rms_min": 2.5,
  "rms_max": 5.0,
  "power_threshold": 0.5,
  "freq_min": 4.0,
  "freq_max": 6.0,
  "severity_thresholds": [2.5, 3.0, 3.5, 4.0]
}
```

### 7.4 批量上传参数

| 参数 | 值 | 说明 |
|------|-----|------|
| BATCH_SIZE | 10 | 触发上传的数据条数 |
| BATCH_TIMEOUT_MS | 30000 | 超时自动上传 (30秒) |
| OFFLINE_BUFFER_SIZE | 50 | 离线缓存容量 |
| HTTP_TIMEOUT_MS | 10000 | HTTP 请求超时 |
| RETRY_COUNT | 3 | 失败重试次数 |

### 7.5 心跳机制

```cpp
HEARTBEAT_INTERVAL_MS = 60000  // 60秒间隔
HEARTBEAT_ENABLED = true
```

---

## 8. 配置系统

### 8.1 编译时配置 (tremor_config.h)

```cpp
// FFT 参数 (不可运行时修改)
#define FFT_SAMPLES             256
#define SAMPLE_RATE             125

// 检测默认值 (可被运行时配置覆盖)
#define TREMOR_RMS_MIN          2.5f
#define TREMOR_RMS_MAX          5.0f
#define TREMOR_POWER_THRESHOLD  0.5f
#define TREMOR_FREQ_MIN         4.0f
#define TREMOR_FREQ_MAX         6.0f
```

### 8.2 运行时配置结构

```cpp
// tremor_config.h
typedef struct {
    float rmsMin;              // RMS 下限阈值 (g)
    float rmsMax;              // RMS 上限阈值 (g)
    float powerThreshold;      // 功率阈值
    float freqMin;             // 频率下限 (Hz)
    float freqMax;             // 频率上限 (Hz)
    float severityThresholds[4]; // 严重度分级阈值
    int configVersion;         // 配置版本号
} TremorRuntimeConfig;

extern TremorRuntimeConfig tremorConfig;
```

### 8.3 配置同步流程

**上传配置 (设备 → 云端):**
```
1. 串口输入 "cfgup"
2. configSyncUploadToCloud()
3. POST /api/config/upload
4. 云端保存配置
```

**拉取配置 (云端 → 设备):**
```
1. 串口输入 "update"
2. configSyncFromCloud()
3. GET /api/config/current
4. 解析 JSON
5. tremorConfigUpdate()
6. 立即生效
```

### 8.4 配置便捷宏

```cpp
// 运行时参数访问 (推荐使用)
#define TREMOR_RT_RMS_MIN           (tremorConfig.rmsMin)
#define TREMOR_RT_RMS_MAX           (tremorConfig.rmsMax)
#define TREMOR_RT_POWER_THRESHOLD   (tremorConfig.powerThreshold)
#define TREMOR_RT_FREQ_MIN          (tremorConfig.freqMin)
#define TREMOR_RT_FREQ_MAX          (tremorConfig.freqMax)
#define TREMOR_RT_SEVERITY_0        (tremorConfig.severityThresholds[0])
// ...
```

---

## 9. 串口命令

### 9.1 基础命令

| 命令 | 功能 | 示例输出 |
|------|------|---------|
| `test` | 运行完整硬件测试 | I2C/WHO_AM_I/初始化/数据读取 |
| `scan` | 扫描 I2C 总线 | 发现设备: 0x68 <-- MPU6050 |
| `read` | 读取传感器数据 | 加速度 X=0.02g Y=0.01g Z=1.00g |
| `stream` | 连续数据输出 | A:320,128,16384 G:10,5,2 T:3200 |
| `reset` | 复位 MPU6050 | [MPU6050] 复位完成 |
| `help` | 显示帮助 | 列出所有命令 |

### 9.2 震颤检测命令

| 命令 | 功能 | 说明 |
|------|------|------|
| `tremor` | 开始/停止连续检测 | 每 2.5 秒分析一次 |
| `analyze` | 执行单次分析 | 显示详细报告 |
| `spectrum` | 显示频谱数据 | 调试用 FFT 结果 |
| `stats` | 显示统计信息 | 检出率、平均频率等 |
| `config` | 显示运行时配置 | 所有阈值参数 |

### 9.3 网络命令

| 命令 | 功能 | 说明 |
|------|------|------|
| `wifi` | 显示 WiFi 状态 | IP、信号强度、重连次数 |
| `connect` | 连接 WiFi | 使用预设 SSID/密码 |
| `disconnect` | 断开 WiFi | 停止网络功能 |
| `upload` | 显示上传状态 | 队列数、统计信息 |
| `flush` | 强制上传 | 立即上传所有缓存 |
| `server` | 显示服务器配置 | 地址、端口、设备 ID |

### 9.4 配置命令

| 命令 | 功能 | 说明 |
|------|------|------|
| `cfgup` | 上传配置到云端 | POST /api/config/upload |
| `update` | 从云端拉取配置 | GET /api/config/current |

### 9.5 串口参数

```
波特率: 115200
数据位: 8
停止位: 1
校验: 无
```

---

## 10. 数据流与时序

### 10.1 启动流程

```
┌─────────────────────────────────────────────────────────┐
│                      setup()                            │
├─────────────────────────────────────────────────────────┤
│ 1. Serial.begin(115200)          串口初始化             │
│ 2. tremorInit()                  FFT 模块初始化          │
│ 3. tremorSetSensorCallback()     注册传感器回调          │
│ 4. configSyncInit()              配置同步初始化          │
│ 5. wifiInit()                    WiFi 管理器初始化       │
│ 6. wifiConnect(15000)            连接 WiFi (15秒超时)    │
│ 7. httpInit()                    HTTP 客户端初始化       │
│ 8. uploaderInit()                上传器初始化            │
└─────────────────────────────────────────────────────────┘
```

### 10.2 主循环

```
┌─────────────────────────────────────────────────────────┐
│                       loop()                            │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 处理串口命令                                         │ │
│ │ └─ 读取输入 → 解析命令 → 执行处理                    │ │
│ └─────────────────────────────────────────────────────┘ │
│                           │                             │
│ ┌─────────────────────────▼─────────────────────────────┐ │
│ │ 连续数据模式 (if streaming_mode)                     │ │
│ │ └─ 读取传感器 → 格式化输出 → delay(100)              │ │
│ └─────────────────────────────────────────────────────┘ │
│                           │                             │
│ ┌─────────────────────────▼─────────────────────────────┐ │
│ │ 震颤检测模式 (if tremor_mode)                        │ │
│ │ └─ 检查间隔 → tremorAnalyze() → 加入上传队列         │ │
│ └─────────────────────────────────────────────────────┘ │
│                           │                             │
│ ┌─────────────────────────▼─────────────────────────────┐ │
│ │ 网络处理                                             │ │
│ │ ├─ wifiAutoReconnect()   WiFi 自动重连               │ │
│ │ ├─ uploaderProcess()     批量上传处理                │ │
│ │ └─ uploaderHeartbeatCheck() 心跳检测                 │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 10.3 震颤分析时序

```
时间线 (毫秒)
│
0     ├─ 开始采集
      │  ├─ 读取样本 1
8     │  ├─ 读取样本 2
16    │  ├─ 读取样本 3
      │  ├─ ...
2048  │  └─ 读取样本 256 (采集完成)
      │
2050  ├─ 去直流 + 加窗
      │
2055  ├─ FFT 计算
      │
2060  ├─ 频谱分析
      │
2065  ├─ 结果评估
      │
2070  └─ 输出报告 / 加入上传队列
      │
2500  └─ 下一次分析 (间隔 2500ms)
```

### 10.4 数据上传时序

```
数据生成                  缓存队列                  批量上传
    │                        │                        │
    ├─ Result 1 ────────────►├─ [1]                   │
    ├─ Result 2 ────────────►├─ [1,2]                 │
    ├─ Result 3 ────────────►├─ [1,2,3]               │
    │   ...                  │   ...                  │
    ├─ Result 10 ───────────►├─ [1..10] ─────────────►├─ POST /batch
    │                        │                        │
    │                        ├─ (队列清空)            ├─ 响应 200 OK
    │                        │                        │
    ├─ Result 11 ───────────►├─ [11]                  │
    │   ...                  │                        │
```

---

## 附录

### A. 调试开关

```cpp
// network_config.h
#define NETWORK_DEBUG_ENABLED true   // 网络调试输出

// tremor_config.h
// #define TREMOR_DEBUG_ENABLED      // FFT 调试 (取消注释启用)
// #define TREMOR_SHOW_RAW_FFT       // 原始 FFT 数据
```

### B. 错误代码

| 代码 | 含义 |
|------|------|
| -1 | 服务器未配置 |
| -2 | WiFi 未连接 |
| -3 | 无法连接服务器 |
| 200 | 请求成功 |
| 400 | 请求格式错误 |
| 500 | 服务器内部错误 |

### C. LED 指示 (可选扩展)

| 状态 | LED 行为 |
|------|---------|
| 启动中 | 快闪 |
| WiFi 连接中 | 慢闪 |
| 正常运行 | 常亮 |
| 检测到震颤 | 双闪 |
| 错误 | 熄灭 |

---

*文档版本: 1.0*
*最后更新: 2024-12*
*项目: Tremor Guard - 帕金森震颤监测手环*
