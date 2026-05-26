<script setup lang="ts">
import { onMounted } from "vue";

import { API } from "@/api";
import CachedAt from "@/components/CachedAt.vue";
import ErrorMessage from "@/components/ErrorMessage.vue";
import Loading from "@/components/Loading.vue";
import StatsComponent from "@/components/stats/Stats.vue";
import Icon from "@/components/ui/Icon.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
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

onMounted(() => refresh());
</script>

<template>
  <Loading v-if="isRunning" />

  <div v-if="stats">
    <StatsComponent :stats="stats" :function-stats="functionStats" />

    <div class="flex justify-center items-center gap-md mt-lg">
      <button class="btn" @click="refresh">
        <Icon name="refresh" :size="14" />
        Refresh
      </button>
    </div>
    <div class="text-center mt-sm">
      <CachedAt :cached-at="stats.cachedAt" />
    </div>
  </div>

  <ErrorMessage v-if="isError" :error="error" />
</template>
