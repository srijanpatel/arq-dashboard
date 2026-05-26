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
              <router-link :to="{ name: 'job', params: { id: job.jobId } }">{{
                job.jobId
              }}</router-link>
            </td>
            <td>
              {{ job.queueName }}
            </td>
            <td>
              {{ job.function }}
            </td>
            <td>
              <Status :status="job.status"></Status>
            </td>
            <td>
              <Success :success="job.success" :status="job.status"></Success>
            </td>
            <td>
              <ReadableDatetime
                :dt="job.enqueueTime || undefined"
              ></ReadableDatetime>
            </td>
            <td>
              <ReadableDatetime
                :dt="job.startTime || undefined"
              ></ReadableDatetime>
            </td>
            <td>
              <ReadableDatetime
                :dt="job.finishTime || undefined"
              ></ReadableDatetime>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pagination
      :total="jobs.total"
      :currentPage="jobs.currentPage"
      :pageSize="jobs.pageSize"
      @update-page="updatePage"
    ></Pagination>
    <p>({{ jobs.total }} jobs in total)</p>
    <CachedAt :cachedAt="jobs.cachedAt"></CachedAt>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import CachedAt from "@/components/CachedAt.vue";
import Status from "@/components/job/Status.vue";
import Success from "@/components/job/Success.vue";
import Pagination from "@/components/Pagination.vue";
import ReadableDatetime from "@/components/ReadableDatetime.vue";
import { JobsWithPagination } from "@/types";
import { getHumanizedRelativeTime, getLocalDatetime } from "@/utils";

export default defineComponent({
  name: "JobsItem",
  components: {
    Pagination,
    ReadableDatetime,
    Status,
    Success,
    CachedAt,
  },
  props: {
    jobs: {
      type: Object as PropType<JobsWithPagination>,
      required: true,
    },
  },
  emits: ["update-page", "refresh-page"],
  setup(_, context) {
    const updatePage = (page: number) => {
      context.emit("update-page", page);
    };

    const refreshPage = () => {
      context.emit("refresh-page");
    };

    return {
      updatePage,
      refreshPage,
      getHumanizedRelativeTime,
      getLocalDatetime,
    };
  },
});
</script>
