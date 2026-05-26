<script setup lang="ts">
import { useTitle } from "@vueuse/core";
import { onMounted, ref, watchEffect } from "vue";

import Job from "@/components/job/JobWrapper.vue";

const props = defineProps<{ id: string }>();

const jobId = ref(props.id);

function updateTitle() {
  useTitle(`Job:${jobId.value} - ARQ Dashboard`);
}

onMounted(updateTitle);

watchEffect(() => {
  jobId.value = props.id;
  updateTitle();
});
</script>

<template>
  <Job :job-id="jobId" />
</template>
