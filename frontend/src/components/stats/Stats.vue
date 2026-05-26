<script setup lang="ts">
import { computed, ref } from "vue";

import RuntimeChart from "@/components/charts/RuntimeChart.vue";
import SuccessRateChart from "@/components/charts/SuccessRateChart.vue";
import StatCard from "@/components/ui/StatCard.vue";
import { useGlobalState } from "@/store";
import type { FunctionStatsResponse, Stats } from "@/types";

const props = defineProps<{
  stats: Stats;
  functionStats: FunctionStatsResponse | null;
}>();

const state = useGlobalState();
const selectedFunction = ref<string>("");

type FnSortKey = "function" | "count" | "successRate" | "avgRuntimeMs" | "p50RuntimeMs" | "p95RuntimeMs" | "p99RuntimeMs";
const fnSortKey = ref<FnSortKey>("count");
const fnSortAsc = ref(false);

function toggleFnSort(key: FnSortKey) {
  if (fnSortKey.value === key) {
    fnSortAsc.value = !fnSortAsc.value;
  } else {
    fnSortKey.value = key;
    fnSortAsc.value = key === "function";
  }
}

function fnSortArrow(key: FnSortKey): string {
  if (fnSortKey.value !== key) return "";
  return fnSortAsc.value ? " ↑" : " ↓";
}

const sortedFunctions = computed(() => {
  if (!props.functionStats) return [];
  const fns = [...props.functionStats.functions];
  const dir = fnSortAsc.value ? 1 : -1;
  const key = fnSortKey.value;
  return fns.sort((a, b) => {
    let av: number | string, bv: number | string;
    if (key === "function") {
      av = a.function; bv = b.function;
      return av < bv ? -dir : av > bv ? dir : 0;
    } else if (key === "successRate") {
      av = a.count > 0 ? a.successCount / a.count : 0;
      bv = b.count > 0 ? b.successCount / b.count : 0;
    } else {
      av = a[key]; bv = b[key];
    }
    return ((av as number) - (bv as number)) * dir;
  });
});

function formatMs(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${(ms / 60000).toFixed(1)}m`;
}

const selectedBuckets = computed(() => {
  if (!props.functionStats) return [];
  if (selectedFunction.value) {
    const fn = props.functionStats.functions.find(
      (f) => f.function === selectedFunction.value
    );
    return fn?.runtimeBuckets || [];
  }
  // Merge all buckets — just show first function's buckets as default
  if (props.functionStats.functions.length > 0) {
    return props.functionStats.functions[0].runtimeBuckets;
  }
  return [];
});

function successRate(s: number, total: number): string {
  if (total === 0) return "—";
  return `${((s / total) * 100).toFixed(1)}%`;
}
</script>

<template>
  <div class="animate-fade-up">
    <!-- Queue name -->
    <h2 class="mb-lg">{{ state.queue }}</h2>

    <!-- Overview cards -->
    <div class="grid grid-cols-5 mb-xl">
      <StatCard
        label="Queued"
        :value="stats.queuedJobs"
        color="var(--color-text-muted)"
        :to="{ name: 'jobs', query: { status: 'queued' } }"
      />
      <StatCard
        label="Deferred"
        :value="stats.deferredJobs"
        color="var(--color-info)"
        :to="{ name: 'jobs', query: { status: 'deferred' } }"
      />
      <StatCard
        label="In Progress"
        :value="stats.inProgressJobs"
        color="var(--color-accent)"
        :to="{ name: 'jobs', query: { status: 'in_progress' } }"
      />
      <StatCard
        label="Complete"
        :value="stats.completeJobs"
        color="var(--color-success)"
        :to="{ name: 'jobs', query: { status: 'complete' } }"
      />
      <StatCard
        label="Not Found"
        :value="stats.notFoundJobs"
        color="var(--color-warning)"
        :to="{ name: 'jobs', query: { status: 'not_found' } }"
      />
    </div>

    <!-- Throughput -->
    <div v-if="functionStats?.throughput" class="grid grid-cols-3 mb-xl">
      <div class="card">
        <div class="flex items-center gap-sm mb-xs">
          <span class="text-muted text-sm" style="font-family: var(--font-ui);">THROUGHPUT</span>
        </div>
        <div style="font-family: var(--font-heading); font-size: 2rem; font-weight: 700;">
          {{ functionStats.throughput.throughputPerMin }}
        </div>
        <div class="text-muted text-sm">jobs / min</div>
      </div>
      <div class="card">
        <div class="text-muted text-sm mb-xs" style="font-family: var(--font-ui);">LAST 5 MINUTES</div>
        <div style="font-family: var(--font-heading); font-size: 2rem; font-weight: 700;">
          {{ functionStats.throughput.jobsLast5min }}
        </div>
        <div class="text-muted text-sm">jobs completed</div>
      </div>
      <div class="card">
        <div class="text-muted text-sm mb-xs" style="font-family: var(--font-ui);">LAST HOUR</div>
        <div style="font-family: var(--font-heading); font-size: 2rem; font-weight: 700;">
          {{ functionStats.throughput.jobsLastHour }}
        </div>
        <div class="text-muted text-sm">jobs completed</div>
      </div>
    </div>

    <!-- Function Performance -->
    <template v-if="functionStats && functionStats.functions.length > 0">
      <div class="card mb-lg">
        <h3 class="mb-md">Function Performance</h3>
        <div class="table-container">
          <table class="table">
            <thead>
              <tr>
                <th class="sortable" @click="toggleFnSort('function')">Function{{ fnSortArrow('function') }}</th>
                <th class="sortable" @click="toggleFnSort('count')">Calls{{ fnSortArrow('count') }}</th>
                <th class="sortable" @click="toggleFnSort('successRate')">Success Rate{{ fnSortArrow('successRate') }}</th>
                <th class="sortable" @click="toggleFnSort('avgRuntimeMs')">Avg{{ fnSortArrow('avgRuntimeMs') }}</th>
                <th class="sortable" @click="toggleFnSort('p50RuntimeMs')">p50{{ fnSortArrow('p50RuntimeMs') }}</th>
                <th class="sortable" @click="toggleFnSort('p95RuntimeMs')">p95{{ fnSortArrow('p95RuntimeMs') }}</th>
                <th class="sortable" @click="toggleFnSort('p99RuntimeMs')">p99{{ fnSortArrow('p99RuntimeMs') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="fn in sortedFunctions" :key="fn.function">
                <td class="text-mono text-sm">{{ fn.function }}</td>
                <td>{{ fn.count }}</td>
                <td>
                  <div class="flex items-center gap-sm">
                    <div class="progress-bar" style="width: 60px;">
                      <div
                        class="progress-bar-fill"
                        :style="{
                          width: fn.count > 0 ? (fn.successCount / fn.count * 100) + '%' : '0%',
                          background: fn.failureCount > 0 ? 'var(--color-warning)' : 'var(--color-success)',
                        }"
                      ></div>
                    </div>
                    <span class="text-sm">{{ successRate(fn.successCount, fn.count) }}</span>
                  </div>
                </td>
                <td class="text-mono text-sm">{{ formatMs(fn.avgRuntimeMs) }}</td>
                <td class="text-mono text-sm">{{ formatMs(fn.p50RuntimeMs) }}</td>
                <td class="text-mono text-sm">{{ formatMs(fn.p95RuntimeMs) }}</td>
                <td class="text-mono text-sm">{{ formatMs(fn.p99RuntimeMs) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Charts row -->
      <div class="grid grid-cols-2 mb-lg">
        <div class="card">
          <div class="flex justify-between items-center mb-md">
            <h3>Runtime Distribution</h3>
            <select v-model="selectedFunction" class="form-select" style="width: auto; min-width: 160px;">
              <option value="">{{ functionStats.functions[0]?.function }}</option>
              <option v-for="fn in functionStats.functions" :key="fn.function" :value="fn.function">
                {{ fn.function }}
              </option>
            </select>
          </div>
          <RuntimeChart v-if="selectedBuckets.length > 0" :buckets="selectedBuckets" />
          <div v-else class="empty-state"><p>No runtime data</p></div>
        </div>

        <div class="card">
          <h3 class="mb-md">Success / Failure</h3>
          <SuccessRateChart :functions="functionStats.functions" />
        </div>
      </div>
    </template>
  </div>
</template>
