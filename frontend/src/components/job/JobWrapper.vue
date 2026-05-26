<template>
  <Loading v-if="getJobTask.isRunning"></Loading>

  <ErrorMessage
    v-if="getJobTask.isError"
    :error="getJobTask.last?.error"
  ></ErrorMessage>

  <JobComponent
    :job="getJobTask.last.value"
    v-if="getJobTask.last?.value"
  ></JobComponent>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useAsyncTask } from "vue-concurrency";

import { API } from "@/api";
import ErrorMessage from "@/components/ErrorMessage.vue";
import JobComponent from "@/components/job/Job.vue";
import Loading from "@/components/Loading.vue";
import { CachedJob } from "@/types";

export default defineComponent({
  name: "JobWrapper",
  components: {
    Loading,
    ErrorMessage,
    JobComponent,
  },
  props: {
    jobId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const getJobTask = useAsyncTask<CachedJob, [string]>(
      async (_signal, jobId) => {
        return await API.getJob(jobId);
      }
    );

    onMounted(async () => {
      await getJobTask.perform(props.jobId);
    });

    return {
      getJobTask,
    };
  },
});
</script>
