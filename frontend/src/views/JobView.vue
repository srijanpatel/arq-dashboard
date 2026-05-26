<template>
  <Job :jobId="jobId"></Job>
</template>

<script lang="ts">
import { useTitle } from "@vueuse/core";
import { defineComponent, onMounted, ref, watchEffect } from "vue";

import Job from "@/components/job/JobWrapper.vue";

export default defineComponent({
  name: "ArtifactView",
  components: {
    Job,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const jobId = ref<string>(props.id);

    const updateTitle = () => {
      useTitle(`Job:${jobId.value} - ARQ Dashboard`);
    };

    onMounted(() => {
      updateTitle();
    });

    watchEffect(() => {
      jobId.value = props.id;
      updateTitle();
    });

    return { jobId };
  },
});
</script>
