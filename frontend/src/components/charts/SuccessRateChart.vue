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
import type { FunctionRuntime } from "@/types";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

const props = defineProps<{ functions: FunctionRuntime[] }>();
const { isDark } = useTheme();

const chartData = computed(() => ({
  labels: props.functions.map((f) => f.function),
  datasets: [
    {
      label: "Success",
      data: props.functions.map((f) => f.successCount),
      backgroundColor: isDark.value
        ? "rgba(107, 163, 74, 0.7)"
        : "rgba(90, 138, 60, 0.7)",
      borderRadius: 4,
    },
    {
      label: "Failure",
      data: props.functions.map((f) => f.failureCount),
      backgroundColor: isDark.value
        ? "rgba(212, 99, 90, 0.7)"
        : "rgba(196, 75, 63, 0.7)",
      borderRadius: 4,
    },
  ],
}));

const chartOptions = computed(() => ({
  indexAxis: "y" as const,
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
      stacked: true,
      grid: { color: isDark.value ? "#332F2B" : "#EBE3D9" },
      ticks: {
        color: isDark.value ? "#A69B90" : "#8C7E72",
        font: { family: "'Space Mono', monospace", size: 10 },
        stepSize: 1,
      },
      border: { display: false },
    },
    y: {
      stacked: true,
      grid: { display: false },
      ticks: {
        color: isDark.value ? "#A69B90" : "#8C7E72",
        font: { family: "'Space Mono', monospace", size: 11 },
      },
      border: { color: isDark.value ? "#3D3733" : "#E2D9CE" },
    },
  },
}));
</script>

<template>
  <div :style="{ height: Math.max(120, functions.length * 40 + 40) + 'px' }">
    <Bar :key="isDark ? 'dark' : 'light'" :data="chartData" :options="chartOptions" />
  </div>
</template>
