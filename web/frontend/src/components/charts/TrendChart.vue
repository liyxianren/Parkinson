<script setup lang="ts">
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar, Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend
)

const props = defineProps<{
  dateLabels: string[]
  severityData: number[] // Line
  tremorCountData: number[] // Bar
}>()

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  plugins: {
    title: {
      display: true,
      text: '近7日震颤趋势',
      align: 'start' as const,
      font: {
          size: 16,
          weight: 'bold'
      }
    }
  },
  scales: {
    y: {
      type: 'linear' as const,
      display: true,
      position: 'left' as const,
      title: {
          display: true,
          text: '平均严重度'
      },
      min: 0,
      max: 4
    },
    y1: {
      type: 'linear' as const,
      display: true,
      position: 'right' as const,
      title: {
          display: true,
          text: '震颤次数'
      },
      grid: {
        drawOnChartArea: false, // only want the grid lines for one axis to show up
      },
    },
  }
}

const chartData = computed(() => {
  return {
    labels: props.dateLabels,
    datasets: [
      {
        type: 'line' as const,
        label: '平均严重度',
        backgroundColor: '#FB923C', // Orange-400
        borderColor: '#FB923C',
        data: props.severityData,
        yAxisID: 'y',
        tension: 0.3
      },
      {
        type: 'bar' as const,
        label: '震颤次数',
        backgroundColor: '#E5E7EB', // Gray-200
        data: props.tremorCountData,
        yAxisID: 'y1',
        borderRadius: 4
      }
    ]
  }
})
</script>

<template>
  <div class="w-full h-80">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
