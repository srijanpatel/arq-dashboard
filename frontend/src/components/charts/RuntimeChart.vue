<script setup lang="ts">
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  Tooltip,
} from "chart.js";
import { computed } from "vue";
import { Bar } from "vue-chartjs";

import { useTheme } from "@/composables/useTheme";
import type { RuntimeBucket } from "@/types";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const props = defineProps<{ buckets: RuntimeBucket[] }>();
const { isDark } = useTheme();

function formatMs(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}

const chartData = computed(() => ({
  labels: props.buckets.map(
    (b) => `${formatMs(b.rangeStartMs)}-${formatMs(b.rangeEndMs)}`
  ),
  datasets: [
    {
      data: props.buckets.map((b) => b.count),
      backgroundColor: isDark.value
        ? "rgba(224, 144, 80, 0.6)"
        : "rgba(200, 100, 42, 0.6)",
      borderColor: isDark.value ? "#E09050" : "#C8642A",
      borderWidth: 1,
      borderRadius: 4,
    },
  ],
}));

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      backgroundColor: isDark.value ? "#252220" : "#2C2520",
      titleColor: "#E8E0D8",
      bodyColor: "#E8E0D8",
      borderColor: isDark.value ? "#3D3733" : "#E2D9CE",
      borderWidth: 1,
      cornerRadius: 8,
      padding: 10,
    },
    legend: { display: false },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: {
        color: isDark.value ? "#A69B90" : "#8C7E72",
        font: { family: "'Space Mono', monospace", size: 10 },
        maxRotation: 45,
      },
      border: { color: isDark.value ? "#3D3733" : "#E2D9CE" },
    },
    y: {
      grid: { color: isDark.value ? "#332F2B" : "#EBE3D9" },
      ticks: {
        color: isDark.value ? "#A69B90" : "#8C7E72",
        font: { family: "'Space Mono', monospace", size: 10 },
        stepSize: 1,
      },
      border: { display: false },
    },
  },
}));
</script>

<template>
  <div style="height: 240px;">
    <Bar :key="isDark ? 'dark' : 'light'" :data="chartData" :options="chartOptions" />
  </div>
</template>
