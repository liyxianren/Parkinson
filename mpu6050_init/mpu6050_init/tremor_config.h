/**
 * ============================================================
 * tremor_config.h
 * 震颤检测配置参数 / Tremor Detection Configuration
 * ============================================================
 *
 * 项目: 帕金森震颤监测手环 (Tremor Guard)
 * 功能: 定义 FFT 分析和震颤检测的所有配置参数
 *
 * ============================================================
 */

#ifndef TREMOR_CONFIG_H
#define TREMOR_CONFIG_H

// ============================================================
// FFT 参数 (FFT Parameters)
// ============================================================

#define FFT_SAMPLES         256         // 样本数 (必须是2的幂)
                                        // Sample count (must be power of 2)

#define SAMPLE_RATE         125         // 采样率 Hz (与 MPU6050 配置一致)
                                        // Sample rate Hz (matches MPU6050 config)

#define SAMPLE_INTERVAL_MS  8           // 采样间隔 ms (1000/125)
                                        // Sample interval ms

// 频率分辨率 = SAMPLE_RATE / FFT_SAMPLES = 125/256 ≈ 0.488 Hz
// Frequency resolution = SAMPLE_RATE / FFT_SAMPLES ≈ 0.488 Hz

// ============================================================
// 帕金森震颤频率范围 (Parkinson Tremor Frequency Range)
// ============================================================

#define TREMOR_FREQ_MIN     4.0         // 最低频率 Hz (Lower bound)
#define TREMOR_FREQ_MAX     6.0         // 最高频率 Hz (Upper bound)

// 对应 FFT bin 索引 (Corresponding FFT bin indices):
// - Start bin: 4.0 / 0.488 ≈ 8
// - End bin:   6.0 / 0.488 ≈ 12

// ============================================================
// 检测阈值 (Detection Thresholds)
// 基于实际测试校准 (2024-12)
// Calibrated from actual testing
//
// 实测数据:
// - 静止状态: RMS < 0.1g
// - 低级抖动: RMS ≈ 2.5-3.0g
// - 中度抖动: RMS ≈ 3.0-4.0g
// - 剧烈抖动: RMS ≈ 4.0-5.0g+
// ============================================================

#define TREMOR_POWER_THRESHOLD      0.5     // 4-6Hz 频段功率阈值
                                            // Power threshold in 4-6Hz band

#define TREMOR_RMS_MIN              2.5     // RMS 幅度下限 (g) - 低于此值不算震颤
                                            // RMS minimum threshold (g)

#define TREMOR_RMS_MAX              5.0     // RMS 幅度上限 (g) - 高于此值抛弃测试
                                            // RMS maximum threshold (g)

// 兼容旧代码
#define TREMOR_RMS_THRESHOLD        TREMOR_RMS_MIN

// ============================================================
// 严重度阈值 (Severity Thresholds)
// 基于实际测试校准，单位: g (RMS 加速度)
// Calibrated from actual testing, unit: g (RMS acceleration)
//
// 实测校准记录:
// - 静止: RMS < 0.1g → 无震颤
// - 低级抖动: RMS 2.5-3.0g → 轻度 (等级 1-2)
// - 中度抖动: RMS 3.0-4.0g → 中度 (等级 3)
// - 剧烈抖动: RMS 4.0-5.0g → 重度 (等级 4)
// ============================================================

#define SEVERITY_THRESHOLD_0    2.5     // < 2.5g: 无震颤 (None)
#define SEVERITY_THRESHOLD_1    3.0     // 2.5-3.0g: 轻度 (Mild)
#define SEVERITY_THRESHOLD_2    3.5     // 3.0-3.5g: 中轻度 (Mild-Moderate)
#define SEVERITY_THRESHOLD_3    4.0     // 3.5-4.0g: 中度 (Moderate)
                                        // > 4.0g: 重度 (Severe)

// ============================================================
// 加速度计参数 (Accelerometer Parameters)
// 与主程序 mpu6050_init.ino 中的配置一致
// Matches configuration in mpu6050_init.ino
// ============================================================

#define ACCEL_SENSITIVITY   16384.0     // LSB/g (±2g量程)
                                        // LSB/g (±2g range)

// ============================================================
// 震颤检测模式参数 (Tremor Detection Mode Parameters)
// ============================================================

#define TREMOR_ANALYSIS_INTERVAL_MS  2500   // 连续检测模式下的分析间隔 (ms)
                                            // Analysis interval in continuous mode

#define TREMOR_DATA_COLLECTION_TIME  ((FFT_SAMPLES * SAMPLE_INTERVAL_MS))
                                            // 数据采集时间 ≈ 2048ms
                                            // Data collection time ≈ 2048ms

// ============================================================
// 调试选项 (Debug Options)
// ============================================================

// #define TREMOR_DEBUG_ENABLED        // 取消注释以启用详细调试输出
                                        // Uncomment to enable verbose debug output

// #define TREMOR_SHOW_RAW_FFT         // 取消注释以显示原始 FFT 数据
                                        // Uncomment to show raw FFT data

// ============================================================
// 输出格式选项 (Output Format Options)
// ============================================================

#define TREMOR_OUTPUT_DETAILED      1   // 详细报告模式
                                        // Detailed report mode

#define TREMOR_OUTPUT_SIMPLE        0   // 简洁输出模式 (用于连续监测)
                                        // Simple output mode (for continuous monitoring)

// 默认输出模式 / Default output mode
#define TREMOR_DEFAULT_OUTPUT_MODE  TREMOR_OUTPUT_DETAILED

#endif // TREMOR_CONFIG_H
