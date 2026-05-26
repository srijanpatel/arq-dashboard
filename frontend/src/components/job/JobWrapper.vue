<script setup lang="ts">
import { onMounted } from "vue";

import { API } from "@/api";
import ErrorMessage from "@/components/ErrorMessage.vue";
import JobComponent from "@/components/job/Job.vue";
import Loading from "@/components/Loading.vue";
import { useAsyncTask } from "@/composables/useAsyncTask";
import type { CachedJob } from "@/types";

const props = defineProps<{ jobId: string }>();

const { data: job, isRunning, isError, error, perform } = useAsyncTask<CachedJob>(
  () => API.getJob(props.jobId)
);

onMounted(() => perform());
</script>

<template>
  <Loading v-if="isRunning" />
  <ErrorMessage v-if="isError" :error="error" />
  <JobComponent v-if="job" :job="job" />
</template>
