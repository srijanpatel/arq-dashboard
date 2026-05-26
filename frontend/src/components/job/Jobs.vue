<script setup lang="ts">
import CachedAt from "@/components/CachedAt.vue";
import Status from "@/components/job/Status.vue";
import Success from "@/components/job/Success.vue";
import Pagination from "@/components/Pagination.vue";
import ReadableDatetime from "@/components/ReadableDatetime.vue";
import { computed, ref } from "vue";

import type { Job, JobsWithPagination } from "@/types";

const props = defineProps<{ jobs: JobsWithPagination }>();

function runtimeMs(job: Job): number | null {
  if (!job.startTime || !job.finishTime) return null;
  return new Date(job.finishTime).getTime() - new Date(job.startTime).getTime();
}

function fmtRuntime(job: Job): string {
  const ms = runtimeMs(job);
  if (ms === null) return "—";
  if (ms < 1000) return `${ms}ms`;
  const s = ms / 1000;
  if (s < 60) return `${s.toFixed(1)}s`;
  return `${(s / 60).toFixed(1)}m`;
}

type JobSortKey = "jobId" | "function" | "status" | "success" | "enqueueTime" | "runtime";
const sortKey = ref<JobSortKey>("enqueueTime");
const sortAsc = ref(false);

function toggleSort(key: JobSortKey) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value;
  } else {
    sortKey.value = key;
    sortAsc.value = key === "function" || key === "jobId";
  }
}

function sortArrow(key: JobSortKey): string {
  if (sortKey.value !== key) return "";
  return sortAsc.value ? " ↑" : " ↓";
}

const sortedJobs = computed(() => {
  const jobs = [...props.jobs.jobs];
  const dir = sortAsc.value ? 1 : -1;
  const key = sortKey.value;
  return jobs.sort((a, b) => {
    if (key === "runtime") {
      const ar = runtimeMs(a) ?? -1;
      const br = runtimeMs(b) ?? -1;
      return (ar - br) * dir;
    }
    if (key === "success") {
      return ((a.success ? 1 : 0) - (b.success ? 1 : 0)) * dir;
    }
    const av = a[key] ?? "";
    const bv = b[key] ?? "";
    return av < bv ? -dir : av > bv ? dir : 0;
  });
});

const emit = defineEmits<{
  "update-page": [page: number];
  "refresh-page": [];
}>();
</script>

<template>
  <div v-if="jobs.jobs.length === 0" class="empty-state">
    <h3>No jobs to display</h3>
    <p>Try adjusting your filters or check back later.</p>
  </div>
  <div v-else class="animate-fade-up">
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th class="sortable" @click="toggleSort('jobId')">Job ID{{ sortArrow('jobId') }}</th>
            <th>Queue</th>
            <th class="sortable" @click="toggleSort('function')">Function{{ sortArrow('function') }}</th>
            <th class="sortable" @click="toggleSort('status')">Status{{ sortArrow('status') }}</th>
            <th class="sortable" @click="toggleSort('success')">Success{{ sortArrow('success') }}</th>
            <th class="sortable" @click="toggleSort('enqueueTime')">Enqueued{{ sortArrow('enqueueTime') }}</th>
            <th class="sortable" @click="toggleSort('runtime')">Runtime{{ sortArrow('runtime') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in sortedJobs" :key="job.jobId">
            <td>
              <router-link
                class="text-mono text-sm"
                :to="{ name: 'job', params: { id: job.jobId } }"
              >{{ job.jobId.slice(0, 12) }}&hellip;</router-link>
            </td>
            <td class="text-muted text-sm">{{ job.queueName || '—' }}</td>
            <td class="text-mono text-sm">{{ job.function }}</td>
            <td><Status :status="job.status" /></td>
            <td><Success :success="job.success" :status="job.status" /></td>
            <td class="text-sm"><ReadableDatetime :dt="job.enqueueTime || undefined" /></td>
            <td class="text-mono text-sm">{{ fmtRuntime(job) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination
      :total="jobs.total"
      :current-page="jobs.currentPage"
      :page-size="jobs.pageSize"
      @update-page="(p) => emit('update-page', p)"
    />
    <div class="flex justify-between items-center mt-sm">
      <span class="text-muted text-sm">{{ jobs.total }} jobs total</span>
      <CachedAt :cached-at="jobs.cachedAt" />
    </div>
  </div>
</template>
