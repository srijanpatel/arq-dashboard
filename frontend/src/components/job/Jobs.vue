<script setup lang="ts">
import CachedAt from "@/components/CachedAt.vue";
import Status from "@/components/job/Status.vue";
import Success from "@/components/job/Success.vue";
import Pagination from "@/components/Pagination.vue";
import ReadableDatetime from "@/components/ReadableDatetime.vue";
import type { JobsWithPagination } from "@/types";

defineProps<{ jobs: JobsWithPagination }>();

const emit = defineEmits<{
  "update-page": [page: number];
  "refresh-page": [];
}>();

function updatePage(page: number) {
  emit("update-page", page);
}
</script>

<template>
  <div v-if="jobs.jobs.length === 0">
    <article class="message is-info">
      <div class="message-body">There is no job to display</div>
    </article>
  </div>
  <div v-else>
    <div class="table-container">
      <table class="table is-bordered is-fullwidth">
        <thead>
          <tr>
            <th>Job ID</th>
            <th>Queue</th>
            <th>Function</th>
            <th>Status</th>
            <th>Success</th>
            <th>Enqueued time</th>
            <th>Start time</th>
            <th>Finish time</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs.jobs" :key="job.jobId">
            <td>
              <router-link :to="{ name: 'job', params: { id: job.jobId } }">
                {{ job.jobId }}
              </router-link>
            </td>
            <td>{{ job.queueName }}</td>
            <td>{{ job.function }}</td>
            <td><Status :status="job.status" /></td>
            <td><Success :success="job.success" :status="job.status" /></td>
            <td><ReadableDatetime :dt="job.enqueueTime || undefined" /></td>
            <td><ReadableDatetime :dt="job.startTime || undefined" /></td>
            <td><ReadableDatetime :dt="job.finishTime || undefined" /></td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination
      :total="jobs.total"
      :current-page="jobs.currentPage"
      :page-size="jobs.pageSize"
      @update-page="updatePage"
    />
    <p>({{ jobs.total }} jobs in total)</p>
    <CachedAt :cached-at="jobs.cachedAt" />
  </div>
</template>
