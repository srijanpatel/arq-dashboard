<script setup lang="ts">
import CachedAt from "@/components/CachedAt.vue";
import Status from "@/components/job/Status.vue";
import Success from "@/components/job/Success.vue";
import Pagination from "@/components/Pagination.vue";
import ReadableDatetime from "@/components/ReadableDatetime.vue";
import type { Job, JobsWithPagination } from "@/types";

defineProps<{ jobs: JobsWithPagination }>();

function runtime(job: Job): string {
  if (!job.startTime || !job.finishTime) return "—";
  const ms = new Date(job.finishTime).getTime() - new Date(job.startTime).getTime();
  if (ms < 1000) return `${ms}ms`;
  const s = ms / 1000;
  if (s < 60) return `${s.toFixed(1)}s`;
  return `${(s / 60).toFixed(1)}m`;
}

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
            <th>Job ID</th>
            <th>Queue</th>
            <th>Function</th>
            <th>Status</th>
            <th>Success</th>
            <th>Enqueued</th>
            <th>Runtime</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs.jobs" :key="job.jobId">
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
            <td class="text-mono text-sm">{{ runtime(job) }}</td>
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
