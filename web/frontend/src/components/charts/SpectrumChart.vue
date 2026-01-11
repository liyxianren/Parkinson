<script setup lang="ts">
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{
  labels: string[]
  data: number[]
  highlightRange?: [number, number] // e.g. [4, 6] Hz
}>()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    title: {
      display: true,
      text: '频率分布 (FFT)',
      font: {
          size: 14,
          weight: 'normal'
      },
      color: '#6B7280'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      display: false
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
          maxTicksLimit: 10
      }
    }
  }
}

const chartData = computed(() => {
  return {
    labels: props.labels,
    datasets: [
      {
        label: '能量',
        data: props.data,
        backgroundColor: (ctx: any) => {
           // 高亮帕金森特征频段 (4-6Hz)
           const index = ctx.dataIndex
           const freq = parseFloat(props.labels[index])
           if (freq >= 4 && freq <= 6) {
               return '#F97316' // Orange
           }
           return '#E5E7EB' // Gray
        },
        borderRadius: 4
      }
    ]
  }
})
</script>

<template>
  <div class="w-full h-64">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
