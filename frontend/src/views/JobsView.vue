<script setup lang="ts">
import { useTitle } from "@vueuse/core";
import { onMounted } from "vue";

import Jobs from "@/components/job/JobsWrapper.vue";

onMounted(() => useTitle("Jobs - ARQ Dashboard"));
</script>

<template>
  <Jobs />
</template>
