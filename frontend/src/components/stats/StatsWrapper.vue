<script setup lang="ts">
import { onMounted } from "vue";

import { API } from "@/api";
import CachedAt from "@/components/CachedAt.vue";
import ErrorMessage from "@/components/ErrorMessage.vue";
import Loading from "@/components/Loading.vue";
import StatsComponent from "@/components/stats/Stats.vue";
import Icon from "@/components/ui/Icon.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
import { useAutoRefresh, type RefreshInterval } from "@/composables/useAutoRefresh";
import type { FunctionStatsResponse, Stats } from "@/types";

const { data: stats, isRunning, isError, error, perform: fetchStats } = useAsyncTask<Stats>(
  () => API.getStats()
);

const { data: functionStats, perform: fetchFunctionStats } = useAsyncTask<FunctionStatsResponse>(
  () => API.getFunctionStats()
);

async function refresh() {
  await Promise.all([fetchStats(), fetchFunctionStats()]);
}

const { interval, setInterval: setRefreshInterval } = useAutoRefresh(refresh);

const intervals: { label: string; value: RefreshInterval }[] = [
  { label: "Off", value: 0 },
  { label: "10s", value: 10 },
  { label: "30s", value: 30 },
  { label: "60s", value: 60 },
];

onMounted(() => refresh());
</script>

<template>
  <Loading v-if="isRunning && !stats" />

  <div v-if="stats">
    <StatsComponent :stats="stats" :function-stats="functionStats" />

    <div class="flex justify-center items-center gap-md mt-lg">
      <button class="btn" @click="refresh" :disabled="isRunning">
        <Icon name="refresh" :size="14" :class="{ 'spin-icon': isRunning }" />
        Refresh
      </button>
      <div class="flex items-center gap-sm">
        <span class="text-muted text-sm">Auto:</span>
        <button
          v-for="opt in intervals"
          :key="opt.value"
          class="btn btn-ghost"
          :class="{ 'auto-active': interval === opt.value }"
          @click="setRefreshInterval(opt.value)"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>
    <div class="text-center mt-sm">
      <CachedAt :cached-at="stats.cachedAt" />
    </div>
  </div>

  <ErrorMessage v-if="isError" :error="error" />
</template>

<style scoped>
.spin-icon {
  animation: spin 0.7s linear infinite;
}

.auto-active {
  background: var(--color-accent-light);
  color: var(--color-accent);
}
</style>
